import room_dictionary

# from typing import Optional
# from wechaty_puppet import ScanStatus
# from wechaty import Contact, Friendship
# from wechaty.user import Message
# from wechaty import Wechaty
# from wechaty_plugin_contrib.contrib import (
#     RoomInviterOptions,
#     RoomInviterPlugin
# )
#
#
# import constants
# import message_process
# import asyncio
#
# class MyBot(Wechaty):
#     def __init__(self):
#         super().__init__()
#
#     async def on_message(self, msg: Message):
#         talker = msg.talker()
#         wechat_id = talker.contact_id
#         text = msg.text()
#         room = msg.room()
#         await talker.ready()
#         if room is None:
#             print(wechat_id)
#             print("room", room)
#             reply_message = message_process.msg_process(text, wechat_id)
#             print(reply_message)
#             await talker.say(reply_message)
#
#     async def on_friendship(self, friendship: Friendship):
#         print('进来了吗')
#         contact = friendship.contact()
#         await contact.ready()
#
#         await friendship.accept()
#         print('waiting to send message ...')
#         await asyncio.sleep(3)
#         await contact.say(constants.default_msg)
#         print("自动添加", friendship.friendship_id)
#
#     async def on_login(self, contact: Contact):
#         print(f'user: {contact} has login')
#
#     async def on_scan(self, status: ScanStatus, qr_code: Optional[str] = None,
#                       data: Optional[str] = None):
#         contact = self.Contact.load(self.contact_id)
#         print(f'user <{contact}> scan status: {status.name} , '
#               f'qr_code: {qr_code}')
#
#
# async def bot_main():
#     # rules: room_dictionary.Dict
#     bot = MyBot()
#     # plugin = RoomInviterPlugin(options=RoomInviterOptions(
#     #     name='XY',
#     #     rules=rules,
#     #     welcome='欢迎入群'
#     # ))
#     # bot.use(plugin)
#     await bot.start()
