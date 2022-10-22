from sqlalchemy import Column, String, Integer, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Email(Base):
    __tablename__ = 'im_wx_email_verify'
    id = Column(Integer, primary_key=True, autoincrement=True)
    wcId = Column(String(100))
    email = Column(String(100))
    verified = Column(Integer)
    verification_code = Column(String(10))

    def __init__(self, id, wcId, email, verified, verification_code):
        self.id = id
        self.wcId = wcId
        self.email = email
        self.verified = verified
        self.verification_code = verification_code


class AutoReply(Base):
    __tablename__ = 'im_wx_auto_reply'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_wcId = Column(String(100))
    key = Column(String(15))
    value = Column(String(1024))
    type = Column(Integer)
    created_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='创建时间')
    created_by = Column(Integer)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='创建时间')
    updated_by = Column(Integer)
    is_deleted = Column(Integer)


class Message(Base):
    __tablename__ = 'im_wx_send_msg_record'
    id = Column(Integer, primary_key=True, autoincrement=True)
    wId = Column(String(100))
    fromuser = Column(String(100))
    touser = Column(String(100))
    type = Column(String(100))
    content = Column(String(1024))
    origin = Column(Integer)
    created_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='创建时间')
    created_by = Column(Integer)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='创建时间')
    updated_by = Column(Integer)
    is_deleted = Column(Integer)


    def __init__(self, id, wId, fromuser, touser, type, content):
        self.id = id
        self.wId = wId
        self.fromuser = fromuser
        self.touser = touser
        self.type = type
        self.content = content


class Decoder(Base):
    __tablename__ = 'im_wx_user_decoder'
    id = Column(Integer, primary_key=True, autoincrement=True)
    wId = Column(String(100))
    goal_type = Column(Integer)
    gender = Column(Integer)
    birth_year_min = Column(Integer)
    birth_year_max = Column(Integer)
    school = Column(String(20))
    accp_program = Column(String(20))
    hobby = Column(Integer)
    hobby_match = Column(Integer)
    created_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='创建时间')
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='创建时间')

    def __init__(self, id, wId, goal_type, gender, birth_year_min, birth_year_max, school, accp_program, hobby, hobby_match):
        self.id = id
        self.wId = wId
        self.goal_type = goal_type
        self.gender = gender
        self.birth_year_min = birth_year_min
        self.birth_year_max = birth_year_max
        self.school = school
        self.accp_program = accp_program
        self.hobby = hobby
        self.hobby_match = hobby_match


class Encoder(Base):
    __tablename__ = 'im_wx_user_encoder'
    id = Column(Integer, primary_key=True, autoincrement=True)
    wId = Column(String(100))
    goal_type = Column(Integer)
    gender = Column(Integer)
    birth_year = Column(Integer)
    school = Column(String(20))
    program = Column(String(20))
    hobby = Column(Integer)
    max_decoding = Column(Integer)
    contact_pref = Column(String(10))
    created_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='创建时间')
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='创建时间')

    def __init__(self, id, wId, goal_type, gender, birth_year, school, program, hobby, max_decoding, contact_pref):
        self.id = id
        self.wId = wId
        self.goal_type = goal_type
        self.gender = gender
        self.birth_year = birth_year
        self.school = school
        self.program = program
        self.hobby = hobby
        self.max_decoding = max_decoding
        self.contact_pref = contact_pref