# -*- coding:utf-8
# Author: Syaoran@sc33.top
# Plugins name : Character Sfx
# LastUpdate: 29th,Nov,2020


from nonebot import on_command,CommandSession

import sys
import json
from fuzzywuzzy import process


op1 = open('src/data/charasfx/sfx_url.json','r',encoding='utf-8')
data1 = json.load(op1)



def fzwz(chara_ipt):
    op = open('src/data/charasfx/aid.json','r',encoding='utf-8')
    data =json.load(op)
    char_ls = []
    for char in data:
        char_ls.append(char)
    fzwz = process.extractOne(chara_ipt,char_ls)
    if fzwz[1] > 60:
        assetsid = data.get(fzwz[0])
        return assetsid
    else:
        return False



def get_stype(type_ipt):
    if type_ipt=='死亡':
        stype = 'die'
    elif type_ipt=='魂册':
        stype = 'info'
    elif type_ipt=='技能1':
        stype = 'skill_s1'
    elif type_ipt=='技能2':
        stype = 'skill_s2'
    elif type_ipt=='技能3':
        stype = 'skill_s3'
    elif type_ipt=='技能4':
        stype = 'skill_s4'
    elif type_ipt=='攻击':
        stype = 'battle_attack'
    elif type_ipt=='蓄力':
        stype = 'battle_charge'
    elif type_ipt=='受击':
        stype = 'battle_hit'
    elif type_ipt=='剧情':
        stype = 'story'
    elif type_ipt=='结算':
        stype = 'victory'
    else:
        stype = None
    return stype

def sfx_search(assetsid,stype):
    msg_ls = []
    for aid,ls in data1.items():
        for ct in range(len(ls)):
            it = data1.get(aid)[ct]
            sfx_id = it.get('sfx_id')
            name = it.get('name')
            sfx_type = it.get('type')
            if (assetsid != aid) or (stype != sfx_type):
                pass
            else:
                ls = []
                msg = f'{sfx_id}.{name}'
                msg_ls.append(msg)
    result = '\n'.join(msg_ls)
    return result    

def sfx_url(sfx_id_ipt):
    for aid,ls in data1.items():
        for ct in range(len(ls)):
            it = data1.get(aid)[ct]
            sfx_id = it.get('sfx_id')
            url = it.get('url')
            if sfx_id_ipt == sfx_id:
                msg_cq=f'[CQ:record,file={url}]'
            else:
                pass
    return msg_cq

@on_command('charaSfx_search',only_to_me=False,aliases='角色语音查询',shell_like=True)
async def charaSfx_search(session: CommandSession):
    try:
        chara_ipt = session.argv[0]
    except:
        session.finish('您未输入查询的角色')
    try:
        type_ipt = session.argv[1]
    except:
        type_ipt = '魂册'
        session.send('命令不全，自动补充关键词[魂册]')

    if type_ipt in ['死亡','魂册','攻击','受击','蓄力','技能1','技能2','技能3','技能4','剧情','结算']:
        pass
    else:
        session.finish('类型错误，使用帮助-6查看支持的语言类型')

    assetsid = fzwz(chara_ipt)
    stype = get_stype(type_ipt)
    result = sfx_search(assetsid,stype)

    await session.send(result)

@on_command('charSfx',only_to_me=False,aliases='角色语音',shell_like=True)
async def charSfx(session: CommandSession):
    try:
        sfx_id_ipt = int(session.argv[0])
        if sfx_id_ipt == 2100:
            await session.send('我大意了啊,小伙子不讲武德')
    except:
        session.finish('参数错误，请输入数字格式')
    
    msg_cq = sfx_url(sfx_id_ipt)
    await session.send(msg_cq)

@on_command('dialogue_add',only_to_me=False,aliases='角色台词-添加',shell_like=True)
async def dialogue_add(session: CommandSession):
    try:
        sfx_id_ipt = int(session.argv[0])
    except:
        session.finish('参数错误，请输入数字格式')
    try:
        dialogue = session.argv[1]
        await session.send('感谢您提供的语音台词，普吉已经好好记下了')
    except:
        session.finish('您未输入正确的台词喔')

    if dialogue:
        f = open('users/dialogue_user_addition.txt','a+',encoding='utf-8')
        f.write('['+str(sfx_id_ipt)+' | '+dialogue+']\n')
        f.close()

@on_command('sfxegg1',only_to_me=False,aliases='娇喘')
async def sfxegg1(session: CommandSession):
    url = 'https://sdorica.gitee.io/sound_effect/sfx/b0037_info_03_jp.wav'
    await session.send(f'[CQ:record,file={url}]')

@on_command('sfxegg2',only_to_me=False,aliases='噗噗噗')
async def sfxegg2(session: CommandSession):
    url = 'https://sdorica.gitee.io/sound_effect/sfx/b0037_story_001_jp.wav'
    await session.send(f'[CQ:record,file={url}]')

@on_command('sfxegg3',only_to_me=False,aliases='砸瓦鲁多')
async def sfxegg3(session: CommandSession):
    url = 'https://sdorica.gitee.io/sound_effect/sfx/b0037sx_story_038_ver1_jp.wav'
    await session.send(f'[CQ:record,file={url}]')