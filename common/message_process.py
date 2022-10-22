from sqlalchemy.orm import sessionmaker

from config import db_config, constants
from common import email_verification
from entity import models


def is_verified(wechat_id):
    engine = db_config.config_db();
    db_session = sessionmaker(bind=engine)
    session = db_session()

    email = session.query(models.Email).filter(models.Email.wcId == wechat_id).first()
    session.close()
    if email is None:
        return 0
    else:
        return email.verified


def store_verified_code(wechat_id, email, code):
    engine = db_config.config_db();
    db_session = sessionmaker(bind=engine)
    session = db_session()
    email_db = session.query(models.Email).filter(models.Email.wcId == wechat_id).first()
    if email_db is None:
        new_email = models.Email(id=0, wcId=wechat_id, email=email, verified=0, verification_code=code)
        session.add(new_email)
    else:
        update_email = session.query(models.Email).filter(models.Email.wcId == wechat_id).update({"verification_code": code,
                                                                                                  "email": email,
                                                                                                  "verified": 0})
    session.commit()
    session.close()


def get_verified_code_by_email(email):
    engine = db_config.config_db();
    db_session = sessionmaker(bind=engine)
    session = db_session()
    email_db = session.query(models.Email).filter(models.Email.email == email).first()
    return email_db


def is_match_verified(wechat_id, code):
    engine = db_config.config_db();
    db_session = sessionmaker(bind=engine)
    session = db_session()
    email = session.query(models.Email).filter(models.Email.wcId == wechat_id).first()
    result = email.verification_code == code
    if result:
        session.query(models.Email).filter(models.Email.wcId == wechat_id).update({"verified": 1})
        session.commit()
        session.close()
    return result


def send_email_for_verification(wechat_id, email):
    code = email_verification.generate()
    print("code: ", code)
    print("email: ", email)
    try:
        email_verification.send_mail(email, code)
    except:
        return constants.email_sent_failed_msg
    store_verified_code(wechat_id, email, code)
    return constants.email_sent_msg


def get_text_auto_reply(key):
    engine = db_config.config_db();
    db_session = sessionmaker(bind=engine)
    session = db_session()
    auto_reply_msg = session.query(models.AutoReply).filter(models.AutoReply.key == key).order_by(models.AutoReply.created_at.desc()).first()
    session.close()
    if auto_reply_msg is not None:
        print(auto_reply_msg.value)
        if auto_reply_msg.type == 0:
            return 0, auto_reply_msg.value
        else:
            return 1, auto_reply_msg.value
    return 2, None


def has_message(wechat_id):
    engine = db_config.config_db();
    db_session = sessionmaker(bind=engine)
    session = db_session()
    msg = session.query(models.Message).filter(models.Message.wId == wechat_id).first()
    if msg is None:
        return 0
    return 1


def store_message(wechat_id, msg_type, text):
    engine = db_config.config_db();
    db_session = sessionmaker(bind=engine)
    session = db_session()
    new_msg = models.Message(id=0, wId=wechat_id, fromuser='MITCSSA小助手', touser=wechat_id,  type=msg_type, content=text)
    session.add(new_msg)
    session.commit()
    session.close()


async def msg_process(self, message, wechat_id, talker):
    reply_msg = ""
    indicator, value = get_text_auto_reply(message)
    # all message store in database

    if is_verified(wechat_id):
        reply_msg = constants.first_level_text
    elif ".edu" in message or "@" in message:
        if email_verification.is_mit_harvard_email(message):
            reply_msg = send_email_for_verification(wechat_id, message)
        else:
            reply_msg = constants.email_error_msg
    elif len(message)==6:
        if is_match_verified(wechat_id, message):
            reply_msg = constants.verification_success_text
        else:
            reply_msg = constants.verification_failed_text
    elif indicator == 0 or indicator == 1:
        if indicator == 0:
            reply_msg = value
        else:
            room = await self.Room.find(value)
            room.ready()
            room.add(talker)
            print("room:", room.room_id)
    else:
        reply_msg = constants.default_msg
    return reply_msg

