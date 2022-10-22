import asyncio
import os
import sys
from entity import models
from config import db_config
from common import wechaty_bot
from flask import Flask, request, abort
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.dirname(sys.path[0]))
print(sys.path)
app = Flask(__name__)


@app.route('/add_auto_reply', methods=['POST'])
def auto_reply():
    if not request.form or not 'key' in request.form or not 'value' in request.form or not 'type' in request.form:
        abort(400)

    engine = db_config.config_db();
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    new_auto_reply = models.AutoReply(user_wcId="wechat", key=request.form.get('key'),
                                      value=request.form.get('value'), type=request.form.get('type'),
                                      is_deleted=0)
    session.add(new_auto_reply)
    session.commit()
    session.close()
    return "add success"


@app.route('/bot_start')
def bot_start():
    print("1")
    os.environ['WECHATY_PUPPET_SERVICE_TOKEN'] = 'puppet_wxwork_99c5ab36ca86a639'
    asyncio.run(wechaty_bot.bot_main())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
