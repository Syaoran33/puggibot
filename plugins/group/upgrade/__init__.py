# -*- coding: utf-8 -*-
# Author: Syaoran
# Plugins name : Upgrade
# LastUpdate: 8th,Dec,2020

from nonebot import get_bot
from nonebot import on_command,CommandSession
import time
import random

import yaml

data = yaml.load(open('src/settings.yaml',encoding='utf-8'))
group_list = data.get('group').get('event').get('upgrade').get('reminder_list')
master = data.get('manager').get('master')


bot = get_bot()
@on_command('upgrade',aliases=('全局更新','全局维护','维护'),only_to_me=False,shell_like=True)
async def upgrade(session:CommandSession):
    sender = str(session.event.user_id)
    if sender != master:
        session.finish('您的权限不够！')
    tm = str(session.argv[0])
    for group_id in group_list:
        await bot.send_group_msg(group_id=group_id,message=f'噗噗噗,普吉机器人更新维护,预计{tm}')


@on_command('relife',only_to_me=False,aliases=('全局复活','全局重生'),shell_like=True)
async def relife(session:CommandSession):
    sender = str(session.event.user_id)
    if sender != master:
        session.finish('您的权限不够！')
    up = str(session.argv[0])
    for group_id in group_list:
        await bot.send_group_msg(group_id=group_id,message=f'噗噗噗,普吉机器人更新完成,继续为您服务~\n更新了功能:{up}')