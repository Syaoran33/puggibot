# -*- coding:utf-8 -*-
# Author: Syaoran
# LastUpdate: 24th,Nov,2020


from nonebot import on_command, CommandSession
from nonebot import get_bot
from nonebot import on_natural_language, NLPSession, IntentCommand

import random
import json
from fuzzywuzzy import process

import yaml 

data = yaml.load(open('src/settings.yaml',encoding='utf-8'))
groupmsg_banlist = data.get('group').get('event').get('gashapon').get('groupmsg_banlist')
#banlevel = data.get('group').get('event').get('announcement').get('level')


@on_natural_language(keywords={'赋魂'},only_to_me=False)
async def gashapon_nlp(session: NLPSession):
    return IntentCommand(90.0, 'gashapon')


bot = get_bot()
@on_command("gashapon",only_to_me=False)
async def gashapon(session: CommandSession):
    if str(session.event.group_id) not in groupmsg_banlist:
        pass
    else:
        session.finish('管理员禁止了群聊使用，请私聊普吉机器人')
    text = session.ctx["message"][0]["data"]["text"]

    if len(text) > 7:
        session.finish()
    else:
        pass
    
    data = open('src/data/gashapon/pools.json','r',encoding='utf-8')
    pools = json.load(data)
    ls = []
    for pool in pools:
        ls.append(pool)

    def judgefornulluse():
        fzwz = process.extractOne(text,ls)
        match = fzwz[1]
        if match > 60:
            return True
        else :
            return False

    def gacha(pool_name):
        
        prob_ls = []
        one = process.extractOne(pool_name,ls)[0]
        ct = pools.get(one).get('ct')
        prob = pools.get(one).get('prob')

        for pb in prob:
            for a in range(0,pb):
                prob_ls.append(ct)
            ct = ct - 1
        del a

        index_ls = []
        prob_inls = prob_ls[:]
        while 1 in prob_inls:
            prob_inls.remove(1)
            prob_inls.append(2)

        for b in range(0,9):
            idx = random.choice(prob_ls)
            index_ls.append(idx)
        del b
        idx_in = random.choice(prob_inls)
        index_ls.append(idx_in)
        random.shuffle(index_ls)


        item_ls = []
        for index in index_ls:
            level = 'lv'+str(index)
            level_ls = pools.get(one).get(level)
            chara = random.choice(level_ls)
            rank = pools.get(one).get('rank')[ct-index]

            if rank == 'SSR': color ='💛金色--'
            elif rank == 'SR' : color = '💜紫色--'
            elif rank == 'R' : color = '💙蓝色--'
            elif rank == 'N' : color = '🤍白色--'
            item = color + chara
            item_ls.append(item)

        result = '\n'.join(item_ls)

        return one,result

    if judgefornulluse() == True:
        name,result = gacha(text)
        await session.send(name+'结果：')
        await session.send(result)