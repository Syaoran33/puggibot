from nonebot import on_command, CommandSession


import requests
import json

import time

import yaml

data = yaml.load(open('src/settings.yaml',encoding='utf-8'))
groupmsg_perlist = data.get('group').get('event').get('signin').get('groupmsg_perlist')

def quanbaike_prefer():
    url = 'http://www.quanbaike.com/tool/picapi/api/index.php?return=json'

    res = requests.get(url)
    res.encoding = res.apparent_encoding
    data = json.loads(res.text)
    img_url = data.get('imgurl')

    return img_url

def member_init(qq):
    addone = {
        str(qq): '0'
    }
    total  = json.load(open('src/data/signin/cooldown.json','r'))
    total.update(addone)

    data = json.dumps(total)
    with open('src/data/signin/cooldown.json','w') as f:
        f.write(data)
        f.close()

def signin_daily(qq):
    total  = json.load(open('src/data/signin/cooldown.json','r'))
    total[qq] = '1'
    data = json.dumps(total)
    with open('src/data/signin/cooldown.json','w') as f:
        f.write(data)
        f.close()

@on_command('signIn',only_to_me=False,aliases='签到')
async def signIn(session:CommandSession):
    try:
        if str(session.event.group_id) not in groupmsg_perlist:
            session.finish()
    except:
        pass
    user_id = str(session.event.user_id)
    data = json.load(open('src/data/signin/cooldown.json','r'))
    if data.get(user_id) == None:
        member_init(user_id)
    elif data.get(user_id) == '1':
        await session.finish('您今日已经签过到啦~')

    if session.ctx['message_type'] == 'group':
        url = quanbaike_prefer()
        cq_text = f'[CQ:cardimage,file={url}]'
        signin_daily(user_id)
        await session.send(f'[CQ:at,qq={user_id}]这是您的签到奖励')
        await session.send(cq_text)
    else:
        url = quanbaike_prefer()
        cq_text = f'[CQ:image,file={url}]'
        signin_daily(user_id)
        await session.send('这是您的签到奖励')
        await session.send(cq_text)

import nonebot
from nonebot import get_bot

@nonebot.scheduler.scheduled_job('cron',hour='0')
async def signin_clear():
    data = '{"0": "0"}'
    with open('src/data/signin/cooldown.json','w') as f:
        f.write(data)
        f.close()

@on_command('signin_clear_force',only_to_me=False)
async def signin_clear_force(session:CommandSession):
    data = '{"0": "0"}'
    with open('src/data/signin/cooldown.json','w') as f:
        f.write(data)
        f.close()