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