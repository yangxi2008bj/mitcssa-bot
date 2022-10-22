from typing import Optional
from wechaty_puppet import ScanStatus
from wechaty import Contact, Friendship, Room, RoomInvitation
from wechaty.user import Message
from wechaty import Wechaty
from config import constants
from common import message_process


class MyBot(Wechaty):
    def __init__(self):
        super().__init__()

    async def on_message(self, msg: Message):
        talker = msg.talker()
        wechat_id = talker.contact_id
        text = msg.text()
        room = msg.room()
        if room is None:
            indicator, value = message_process.get_text_auto_reply(text)
            is_first_talk = not message_process.has_message(wechat_id)
            message_process.store_message(wechat_id, msg.message_type(), text)
            if message_process.is_verified(wechat_id):
                await talker.ready()
                if indicator == 0 or indicator == 1:
                    if indicator == 0:
                        await talker.say(value)
                    else:
                        room = await self.Room.find(value)
                        if room is None:
                            await talker.say("未找到此群")
                        else:
                            room.ready()
                            room_members = await self.puppet.room_members(room.room_id)
                            if talker.contact_id in room_members:
                                in_room_msg = constants.already_in_room_msg + "群名为：" + value
                                await talker.say(in_room_msg)
                            elif len(room_members) == 500:
                                await talker.say(constants.full_room_msg)
                            else:
                                await room.add(talker)

                else:
                    await talker.ready()
                    await talker.say(constants.default_msg)

            elif ".edu" in text or "@" in text:
                MSMS = ['ruizhu@mit.edu', 'royz21@mit.edu', 'yangxi20@mit.edu',
                        'tony93@mit.edu', 'irisc207@mit.edu', 'kritmate@mit.edu',
                        'ericz28@mit.edu', 'hxjia@mit.edu', 'hnx228@mit.edu',
                        'xiaoyu01@mit.edu', 'chenyz31@mit.edu']
                await talker.ready()
                text.strip()
                if text.lower() in MSMS:
                    await talker.say(constants.hello_msg_msms)
                email_db = message_process.get_verified_code_by_email(text)
                print(email_db)
                if email_db is not None:
                    if email_db.wcId == wechat_id:
                        await talker.say("邮件已发送，请直接查收邮件！")
                    else:
                        await talker.say("该邮箱已经被其他微信账号绑定，如需更改绑定请联系mitcssa.assistant@gmail.com")
                    return
                if message_process.email_verification.is_mit_harvard_email(text):
                    await talker.say(message_process.send_email_for_verification(wechat_id, text))
                else:
                    await talker.say(constants.email_error_msg)
            elif len(text) == 6:
                await talker.ready()
                if message_process.is_match_verified(wechat_id, text):
                    await talker.say(constants.verification_success_text)
                else:
                    await talker.say(constants.verification_failed_text)
            else:
                await talker.ready()
                print('is_first_talk', is_first_talk)
                if is_first_talk:
                    await talker.say(constants.hello_msg)
                else:
                    await talker.say(constants.verification_failed_text)

    async def on_login(self, contact: Contact):
        print(f'user: {contact} has login')

    async def on_scan(self, status: ScanStatus, qr_code: Optional[str] = None,
                      data: Optional[str] = None):
        contact = self.Contact.load(self.contact_id)
        print(f'user <{contact}> scan status: {status.name} , '
              f'qr_code: {qr_code}')


async def bot_main():
    bot = MyBot()
    await bot.start()
