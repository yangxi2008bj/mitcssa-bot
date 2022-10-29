import asyncio
import os
import sys

import en_decoder_game
from entity import models
from config import db_config
from common import wechaty_bot
from flask import Flask, request, abort
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.dirname(sys.path[0]))
print(sys.path)
app = Flask(__name__)


@app.route('/schedule_timer')
def auto_reply():
    asyncio.run(en_decoder_game.tasklist())
    return "add success"


@app.route('/bot_start')
def bot_start():
    print("1")
    os.environ['WECHATY_PUPPET_SERVICE_TOKEN'] = 'puppet_wxwork_f97c1436865dc5a6'
    # os.environ['WECHATY_PUPPET_SERVICE_TOKEN'] = 'puppet_wxwork_99c5ab36ca86a639'
    asyncio.run(wechaty_bot.bot_main())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
