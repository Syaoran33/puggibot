# -*- coding:utf-8 -*-
# Author: Syaoran@sc33.top
# LastUpdate: 24th,Nov,2020

from nonebot import on_command,CommandSession

import json
from fuzzywuzzy import process
import random

import yaml 

data = yaml.load(open('src/settings.yaml',encoding='utf-8'))
groupmsg_banlist = data.get('group').get('event').get('figure').get('groupmsg_banlist')

data = json.load(open('src/data/figure/drawings.json','r',encoding='utf-8'))
charaList = []
for char in data:
    charaList.append(char)

@on_command('figure',only_to_me=False,shell_like=True,aliases='立绘')
async def figure(session: CommandSession):
    if str(session.event.group_id) not in groupmsg_banlist:
        pass
    else:
        session.finish('管理员禁止了群聊使用，请私聊普吉机器人')

    try:
        argv_chara = session.argv[0]
    except:
        session.finish()
    try:
        argv_type = session.argv[1]
    except:
        argv_type = '0'
    try:
        argv_no = session.argv[2]
    except:
        argv_no = '0'

    fzwz = process.extractOne(argv_chara,charaList)
    if fzwz[1] > 75:
        chara = fzwz[0]
    else:
        await session.finish('未找到该角色信息,请重试')

    if argv_type == '0':
        try:
            picUrl = data.get(chara).get('picUrl')
        except:
            picUrl = data.get(chara)[3].get('picUrl')

    elif (argv_type == '一阶') or (argv_type =='1'):
        picUrl = data.get(chara)[0].get('picUrl')
    elif (argv_type == '二阶') or (argv_type =='2'):
        picUrl = data.get(chara)[1].get('picUrl')
    elif (argv_type == '三阶') or (argv_type =='3'):
        picUrl = data.get(chara)[2].get('picUrl')
    elif (argv_type == '技能书') or (argv_type == 'alt') or (argv_type == 'Alt'):
        picUrl = data.get(chara)[3].get('picUrl')
    elif (argv_type == '造型书') or (argv_type == 'skin') or (argv_type == 'Skin'):
        if (argv_no == '1') or (argv_no == '0'):
            picUrl = data.get(chara)[4].get('picUrl')
        elif argv_no == '2':
            picUrl = data.get(chara)[5].get('picUrl')
        else:
            await session.finish('输入角色造型书序号错误,请重试')
    else:
        await session.finish('角色立绘类型错误,请重试')

    try:
        imgText = '[CQ:image,file={}]'.format(picUrl)
        await session.send(imgText)
    except:
        await session.finish('服务器错误,请求过于频繁！')


@on_command('setu',only_to_me=False,aliases=('色图','涩图'))
async def setu(session:CommandSession):
    cq_text1 = '[CQ:image,type=flash,file=https://gitee.com/sdorica/puggibot/raw/master/public/img/setu.png]'
    cq_text2 = '[CQ:image,type=show,file=https://gitee.com/sdorica/puggibot/raw/master/public/img/setu.png]'
    cq_text = random.choice((cq_text1,cq_text2))
    await session.send(cq_text)
