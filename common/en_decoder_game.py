from sqlalchemy.orm import sessionmaker

from config import db_config
import re
import math
import schedule
import models
import time


def is_encoder_game(text):
    return re.match('^\(E', text)


def is_decoder_game(text):
    return re.match('^\(D', text)


def is_en_decoder(text):
    encoder_matcher = re.search(
        '\((E), (0|1|-1), (0|1), (0|1|-1), (\d{4}), (M|H), (U|M|D|P), (\d{5}), (-1|\d*), (W|E)\)', text)
    decoder_matcher = re.search(
        '\((D), (0|1|-1), (0|1|-1), (\d{4}), (\d{4}), (M|H|MH), (U|M|D|P|[U|M|D|P][U|M|D|P]|[U|M|D|P][U|M|D|P][U|M|D|P]|[U|M|D|P][U|M|D|P][U|M|D|P][U|M|D|P]), (\d{5}), (1|-1)\)',
        text)
    if encoder_matcher:
        return 0
    elif decoder_matcher:
        return 1
    else:
        return -1


def encoder_process(text, wechat_id):
    encoder_matcher = re.search(
        '\((E), (0|1|-1), (0|1), (0|1|-1), (\d{4}), (M|H), (U|M|D|P), (\d{5}), (-1|\d*), (W|E)\)', text)
    encoder = models.Encoder(wId=wechat_id, goal_type=encoder_matcher.group(2), gender=encoder_matcher.group(3),
                             gender_filter=encoder_matcher.group(4), birth_year=encoder_matcher.group(5),
                             school=encoder_matcher.group(6),
                             program=encoder_matcher.group(7), hobby=encoder_matcher.group(8),
                             max_decoding=encoder_matcher.group(9), contact_pref=encoder_matcher.group(10))
    ret_val = store_encoder(encoder)
    print(ret_val)
    return ret_val


def decoder_process(text, wId):
    decoder_matcher = re.search(
        '\((D), (0|1|-1), (0|1|-1), (\d{4}), (\d{4}), (M|H|MH), (U|M|D|P|[U|M|D|P][U|M|D|P]|[U|M|D|P][U|M|D|P][U|M|D|P]|[U|M|D|P][U|M|D|P][U|M|D|P][U|M|D|P]), (\d{5}), (1|-1)\)',
        text)
    decoder = models.Decoder(wId=wId, goal_type=int(decoder_matcher.group(2)), gender=int(decoder_matcher.group(3)),
                             birth_year_min=int(decoder_matcher.group(4)), birth_year_max=int(decoder_matcher.group(5)),
                             school=decoder_matcher.group(6), accp_program=decoder_matcher.group(7),
                             hobby=int(decoder_matcher.group(8)), hobby_match=int(decoder_matcher.group(9)))
    engine = db_config.config_db();
    db_session = sessionmaker(bind=engine)
    session = db_session()
    limit_encoder = session.query(models.Limit).filter(models.Limit.wId == wId).first()
    candidate = None

    if limit_encoder and limit_encoder.is_decoder > 0:

        candidate = filter_score(decoder)
        print('can1', candidate)
        if candidate:
            update_encoder_decoder_limitation(candidate)
    return candidate


def update_decoder_limitation(decoder):
    engine = db_config.config_db();
    db_session = sessionmaker(bind=engine)
    session = db_session()
    limit_decoder = session.query(models.Limit).filter(models.Limit.wId == decoder.wId).first()
    if limit_decoder:
        session.query(models.Limit).filter(models.Limit.wId == decoder.wId).update(
            {
                "is_decoder": limit_decoder.is_decoder - 1,
            }
        )


def update_encoder_decoder_limitation(encoder):
    engine = db_config.config_db();
    db_session = sessionmaker(bind=engine)
    session = db_session()
    limit_decoder = session.query(models.Limit).filter(models.Limit.wId == encoder.wId).first()
    if limit_decoder and limit_decoder.decoder_count != -1:
        session.query(models.Limit).filter(models.Limit.wId == encoder.wId).update(
            {
                "decoder_count": limit_decoder.decoder_count - 1,
            }
        )
    session.commit()
    session.close()


def store_encoder(encoder):
    engine = db_config.config_db();
    db_session = sessionmaker(bind=engine)
    session = db_session()
    encoders = session.query(models.Encoder).filter(models.Encoder.wId == encoder.wId).first()
    limit_encoder = session.query(models.Limit).filter(models.Limit.wId == encoder.wId).first()
    print(limit_encoder)
    if encoders and limit_encoder and limit_encoder.is_encoder > 0:
        session.query(models.Encoder).filter(models.Encoder.wId == encoder.wId).update(
            {"goal_type": encoder.goal_type,
             "gender": encoder.gender,
             "gender_filter": encoder.gender_filter,
             "birth_year": encoder.birth_year,
             "school": encoder.school,
             "program": encoder.program,
             "hobby": encoder.hobby,
             "max_decoding": encoder.max_decoding,
             "contact_pref": encoder.contact_pref})
        session.query(models.Limit).filter(models.Limit.wId == encoder.wId).update(
            {
                "is_encoder": limit_encoder.is_encoder - 1,
                "decoder_count": encoder.max_decoding
            }
        )
    elif encoders and limit_encoder and limit_encoder.is_encoder <= 0:
        return "limit_max"
    else:
        session.add(encoder)
        limit_new = models.Limit(wId=encoder.wId, is_encoder=0, is_decoder=1, decoder_count=encoder.max_decoding)
        session.add(limit_new)
    session.commit()
    session.close()
    return "success"


def get_email(candidate):
    engine = db_config.config_db();
    db_session = sessionmaker(bind=engine)
    session = db_session()
    email = session.query(models.Email).filter(models.Email.wcId == candidate.wId).first()
    if email:
        return email.email
    return None


def eucl_distance(encoder, decoder):
    if decoder.goal_type != -1 and decoder.goal_type != encoder.goal_type:
        print("goal_type not match")
        return None
    if encoder.gender_filter != -1 and decoder.gender != encoder.gender_filter:
        print("gender not match")
        return None
    if encoder.birth_year < decoder.birth_year_min or encoder.birth_year > decoder.birth_year_max:
        print("birth not match")
        return None
    if decoder.school != 'MH' and decoder.school != encoder.school:
        print("school not match")
        return None

    if encoder.program not in decoder.accp_program:
        print("program not match")
        return None
    ori = str(encoder.hobby);
    cur = str(decoder.hobby);

    res = math.sqrt(math.pow(int(ori[0]) - int(cur[0]), 2) + math.pow(int(ori[1]) - int(cur[1]), 2) + math.pow(int(ori[2]) - int(cur[2]), 2) + pow(
                int(ori[3]) - int(cur[3]), 2) + pow(int(ori[4]) - int(cur[4]), 2))
    return res;


def filter_score(decoder):
    engine = db_config.config_db();
    db_session = sessionmaker(bind=engine)
    session = db_session()
    encoders = session.query(models.Encoder).filter(models.Encoder.wId != decoder.wId)
    session.close()
    candidate = None
    if decoder.hobby_match == 1:
        temp_score = 100
        candidate = encoders[0]
        for encoder in encoders:
            encoder_limit = get_encoder_decoder_limit(encoder)
            if (not is_matched_before(decoder, encoder)) and encoder_limit and (
                    encoder_limit.decoder_count == -1 or encoder_limit.decoder_count > 0):
                res = eucl_distance(encoder, decoder)
                print("eucl:", res)
                if res and res < temp_score:
                    temp_score = res
                    candidate = encoder
    else:
        temp_score = 0
        candidate = encoders[0]
        for encoder in encoders:
            if (not is_matched_before(decoder, encoder)) and get_encoder_decoder_limit and (get_encoder_decoder_limit == -1 or get_encoder_decoder_limit > 0):
                res = eucl_distance(encoder, decoder)
                if res and res > temp_score:
                    temp_score = res
                    candidate = encoder
    if is_matched_before(candidate, decoder):
        return None
    store_matching(decoder, candidate)
    return candidate


def get_encoder_decoder_limit(encoder):
    engine = db_config.config_db();
    db_session = sessionmaker(bind=engine)
    session = db_session()
    encoder_decoder_limit = session.query(models.Limit).filter(models.Limit.wId == encoder.wId).first()
    session.close()
    return encoder_decoder_limit


def is_matched_before(decoder, encoder):
    engine = db_config.config_db();
    db_session = sessionmaker(bind=engine)
    session = db_session()
    res1 = session.query(models.Matching).filter(models.Matching.wId_encoder == decoder.wId,
                                                 models.Matching.wId_decoder == encoder.wId).first()
    res2 = session.query(models.Matching).filter(models.Matching.wId_decoder == decoder.wId,
                                                 models.Matching.wId_encoder == encoder.wId).first()
    session.close()
    if res1 or res2:
        return True;
    return False


def store_matching(decoder, encoder):
    engine = db_config.config_db();
    db_session = sessionmaker(bind=engine)
    session = db_session()
    res1 = session.query(models.Matching).filter(models.Matching.wId_encoder == decoder.wId,
                                                 models.Matching.wId_decoder == encoder.wId).first()
    res2 = session.query(models.Matching).filter(models.Matching.wId_decoder == decoder.wId,
                                                 models.Matching.wId_encoder == encoder.wId).first()
    if res1 or res2:
        session.close()
        return
    else:
        new_matching = models.Matching(wId_encoder=encoder.wId, wId_decoder=decoder.wId)
        session.add(new_matching)
        session.commit()
        session.close()
    return


def reset_count():
    print("I am resetting the count")
    engine = db_config.config_db();
    db_session = sessionmaker(bind=engine)
    session = db_session()
    res = session.query(models.Limit).all()
    print("res", res)
    if res:
        for tmp in res:
            local = session.query(models.Encoder).filter(models.Encoder.wId == tmp.wId).first()
            session.query(models.Limit).filter(models.Limit.wId == tmp.wId).update(
                {
                    "is_encoder": 1,
                    "is_decoder": 1,
                    "decoder_count": local.max_decoding
                }
            )
    session.commit()
    session.close()


def tasklist():
    # clear the schedule
    schedule.clear()
    # schedule.every().saturday.at("23:59").do(reset_count())
    print("i am doing the task")
    schedule.every().saturday.at("23:59").do(reset_count)
    while True:
        schedule.run_pending()  # 运行所有可以运行的任务
        time.sleep(1)

