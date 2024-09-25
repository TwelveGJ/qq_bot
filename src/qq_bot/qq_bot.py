import os
import time
import yaml
import botpy
from botpy import logging
from botpy.message import GroupMessage
from botpy.types.message import MarkdownPayload, MessageMarkdownParams

from src.utils.api_60s import get_60s, get_history_today

# region basic
_bot_info = None
_bot_cmd = None

with open('config/qq_bot/bot_info.yaml') as f:
    _bot_info = yaml.safe_load(f)
with open('src/qq_bot/cmd.yaml') as f:
    _bot_cmd = yaml.safe_load(f)

client_instance = None

_log = logging.get_logger()
# endregion

# region cmd
async def cmd_help(message: GroupMessage):
    content = '命令列表:\n'
    for k, v in _bot_cmd.items():
        content += f'{k} {v["用例"]}\n'
    await message.reply(content=content)

async def cmd_60s(message: GroupMessage):
    content = await get_60s()
    await message.reply(content=content)

async def cmd_history_today(message: GroupMessage):
    content = await get_history_today()
    await message.reply(content=content)

async def cmd_chat(message: GroupMessage):
    content = '暂未开放 Chat 功能'
    await message.reply(content=content)
# endregion

# region func
async def parse_cmd(message: GroupMessage):
    content = message.content.strip()
    for k, v in _bot_cmd.items():
        if content.startswith(k):
            func = globals().get(v['函数名'])
            await func(message)
            return 
    await message.reply(content='无效命令')
    return 
# endregion

# region bot_main

# 由于每月主动推送信息限额仅有4条，因此不再使用主动推送的方式，改为被动回复的方式
# 主动回复方式  await self.api.post_group_message(group_openid=_group_openid, msg_type=0, content=content)
# 被动回复方式  await message._api.post_group_message(group_openid=message.group_openid, msg_type=0, msg_id=message.id, content=content)

class QQBot(botpy.Client):

    async def on_ready(self):
        _log.info('Bot is ready!')


    async def on_group_at_message_create(self, message: GroupMessage):
        # 调用解析命令的函数
        await parse_cmd(message)

    # async def on_ready(self):
    #     print('Bot is ready!')
    #     # Start the periodic task
    #     asyncio.create_task(self.periodic_send_60s())

    # async def periodic_send_60s(self):
    #     while True:
    #         now = time.localtime(time.time() + 8 * 3600)  # Adjust for the 8-hour difference
    #         if now.tm_hour == 9 and now.tm_min == 0:
    #             await self.send_60s_content()
    #             await asyncio.sleep(3600*23)  # Sleep for 60 seconds to avoid multiple triggers within the same minute
    #         await asyncio.sleep(10)  # Check every 30 seconds

intents = botpy.Intents(public_messages=True)
client_instance = QQBot(intents=intents, is_sandbox=True)
client_instance.run(appid=_bot_info['appid'], secret=_bot_info['appsecret'])
# endregion
