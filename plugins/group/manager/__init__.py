# -*- coding:utf-8 -*-
# Author: Syaoran@sc33.top
# Plugins name : Group Manager
# LastUpdate: 28th,Nov,2020

from nonebot import on_request, RequestSession
from nonebot import on_notice, NoticeSession
from nonebot import get_bot

bot = get_bot()

import yaml
import random

data = yaml.load(open('src/settings.yaml',encoding='utf-8'))
self_id = data.get('manager').get('self_id')
groupid_list = data.get('group').get('common_groupid_list')
self_groupid = data.get('group').get('self_group').get('id')
reject = data.get('group').get('self_group').get('reject')
reject_text = data.get('group').get('self_group').get('reject-text')
secret = data.get('group').get('self_group').get('secret')

@on_request('group')
async def approval(session: RequestSession):
    if session.event.comment == secret:
        await session.approve()
    else:
        if reject:
            await session.reject(reject_text)
        else:
            pass

@on_notice('group_increase')
async def welcome(session: NoticeSession):
    user_id = session.event.user_id
    for groupid in groupid_list:
        if str(session.event.group_id) == groupid:
            await session.send('[CQ:at,qq={}]噗噗噗，欢迎新朋友加入～'.format(user_id))


@on_notice('notify')
async def honor(session: NoticeSession):
    if session.event.honor_type == 'talkative':
        user_id = session.event.user_id
        group_mber = await bot.get_group_member_info(group_id=session.event.group_id, user_id=user_id)
        nickname = group_mber['card'] or group_mber['nickname']
        if str(user_id) == self_id:
            lw_text = ['呼风唤雨','84消毒','巨星排面']
            text = random.choice(lw_text)
            await session.send(text)
        else:
            await session.send(f'噗噗噗，恭喜群成员{nickname}成功当上了水龙王,继续加油保持喔~')
    else:
        pass