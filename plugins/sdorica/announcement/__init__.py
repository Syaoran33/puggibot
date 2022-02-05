# -*- coding:utf-8 -*-
# Author: K7cl@k7cl.com

from nonebot import on_command, CommandSession
from nonebot import get_bot
from nonebot import on_natural_language, NLPSession, IntentCommand
import json
import re
import requests

import yaml 

data = yaml.load(open('src/settings.yaml',encoding='utf-8'))
groupmsg_banlist = data.get('group').get('event').get('announcement').get('groupmsg_banlist')
#banlevel = data.get('group').get('event').get('announcement').get('level')

bot = get_bot()

@on_natural_language(keywords={'公告-'},only_to_me=False)
async def anno_nlp(session: NLPSession):
    # 返回意图命令，前两个参数必填，分别表示置信度和意图命令名
    return IntentCommand(90.0, 'anno')


@on_command("anno", only_to_me=False, aliases=('公告','最新公告'))
async def anno(session: CommandSession):
    if str(session.event.group_id) not in groupmsg_banlist:
        pass
    else:
        session.finish('管理员禁止了群聊使用，请私聊普吉机器人')
        
    text = session.ctx["message"][0]["data"]["text"]
    try:
        p = r'(?<=公告-).+'
        pattern = re.compile(p)
        matcher1 = re.search(pattern,text)
        num = int(matcher1.group(0))
        await session.send('第' + str(num) + '条公告：')
        num = num - 1
    except:
        await session.send('最新公告：')
        num = 0

    response = requests.get("https://exp-sermo-sdorica.dragonest.com/v1/sdorica-game/news?locale=zh_CN")
    annodic = json.loads(response.text)
    try:
        annoresult = annodic[num]["content"]
        await session.send(annodic[num]["title"])
        await session.send(annoresult)
    except:
        await session.send('公告获取失败')


@on_natural_language(keywords={'国际公告-'},only_to_me=False)
async def annointer_nlp(session: NLPSession):
    # 返回意图命令，前两个参数必填，分别表示置信度和意图命令名
    if session.event.group_id in groupmsg_banlist:
        session.finish('管理员禁止了群聊使用，请私聊普吉机器人')
    else:
        return IntentCommand(90.0, 'annointer')


@on_command("annointer", only_to_me=False, aliases=('国际公告','annoncement'))
async def annointer(session: CommandSession):
    if session.event.group_id in groupmsg_banlist:
        session.finsh()
    else:
        pass
    text = session.ctx["message"][0]["data"]["text"]
    try:
        p = r'(?<=国际公告-).+'
        pattern = re.compile(p)
        matcher1 = re.search(pattern,text)
        num = int(matcher1.group(0))
        await session.send('第' + str(num) + '条国际公告：')
        num = num - 1
    except:
        await session.send('最新国际公告：')
        num = 0


    response = requests.get("https://1x0x0-api-sermo.rayark.net/v1/sdorica-game/news?locale=zh_CN")
    annodic = json.loads(response.text)
    try:
        annoresult = annodic[num]["content"]
        await session.send(annodic[num]["title"])
        await session.send(annoresult)
    except:
        await session.send('国际公告获取失败')



