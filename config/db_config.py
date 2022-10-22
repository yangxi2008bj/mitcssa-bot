from sqlalchemy import Column, String, create_engine

def config_db():
    return create_engine('mysql+pymysql://root:wechatbotpass@45.79.175.210:3306/wechatbotbase');