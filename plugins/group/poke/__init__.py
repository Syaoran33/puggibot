# -*- coding: utf-8 -*-
# Author: Syaoran@sc33.top
# Plugins name : Poke Me?
# LastUpdate: 29th,Nov,2020


from nonebot import on_notice, NoticeSession
import time
import random

import yaml

data = yaml.load(open('src/settings.yaml',encoding='utf-8'))
self_id = data.get('manager').get('self_id')
master = data.get('manager').get('master')

poke_list = ['不肝，爬','夺笋啊~','让你喜欢上了，我真是罪过的雄鸟','姐姐，我真的不想努力了，呜呜...','Via Soul~','普吉不发威当我牛角面包','不是漂亮美眉不要碰我','小哥哥这样说，手抓又那么紧，是要跟我交朋友吗~','(你有男朋友！？原来我不是你的唯一？所以我们这几天的感情都是假的？)','还戳我,那我们之间没什么好说的了(模仿葇拉)','以貌取人，汝太肤浅了(一二三普吉揍人~)','我错了，你不是太天真，而是可笑！(模仿姨母中)','我的秘制粽子好吃吧！哎呀，你把我绑起来干嘛？','我不是应急食品，你不要过来啊','再戳，我可就要喊小弟庞来揍你了','我的开关不在这里啦(脸红','[CQ:image,file=https://gitee.com/sdorica/puggibot/raw/master/public/img/poke_angry.jpg]','[CQ:record,file=https://sdorica.gitee.io/sound_effect/sfx/b0037_story_013_jp.wav]']


@on_notice('notify')
async def pokeme(session: NoticeSession):
    sender = str(session.event.sender_id)
    target = str(session.event.target_id)
    if target == self_id:
        if session.event.group_id: #水群限制
            if random.choice((True,True,False,True)): 
                if sender == master:
                    timestamp = time.time()
                    localform = time.localtime(timestamp)
                    nowhour = localform.tm_hour
                    hello_list = ['凌晨好', '凌晨好', '凌晨好', '凌晨好', '凌晨好', '凌晨好', '早上好', '早上好', '早上好', '早上好', '早上好', '中午好', '中午好', '中午好', '下午好', '下午好', '下午好', '下午好', '下午好', '晚上好', '晚上好', '晚上好', '晚上好', '晚上好']
                    poke_return = '噗噗噗,'+ hello_list[nowhour] + '主人~'
                    await session.send(poke_return)
                else:
                    poke_return = random.choice(poke_list)
                    await session.send(poke_return)
            else:
                sender_id = session.event['sender_id']
                cq_text = f'[CQ:poke,qq={sender_id}]'
                await session.send(cq_text)
            
        else:
            if sender == master:
                timestamp = time.time()
                localform = time.localtime(timestamp)
                nowhour = localform.tm_hour
                hello_list = ['凌晨好', '凌晨好', '凌晨好', '凌晨好', '凌晨好', '凌晨好', '早上好', '早上好', '早上好', '早上好', '早上好', '中午好', '中午好', '中午好', '下午好', '下午好', '下午好', '下午好', '下午好', '晚上好', '晚上好', '晚上好', '晚上好', '晚上好']
                poke_return = '噗噗噗,'+ hello_list[nowhour] + '主人~'
                await session.send(poke_return)
            else:
                poke_return = random.choice(poke_list)
                await session.send(poke_return)