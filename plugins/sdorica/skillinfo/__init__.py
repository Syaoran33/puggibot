# -*- coding: utf-8 -*-
# Author: Syaoran,Xenokip
# LastUpdate: 1st,Dec,2020

from nonebot import on_command,CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
import json
import sys
import base64
from fuzzywuzzy import process
import yaml

data = yaml.load(open('src/settings.yaml',encoding='utf-8'))
groupmsg_banlist = data.get('group').get('event').get('skillinfo').get('groupmsg_banlist')

op1 = open('src/data/skillinfo/skillInfo','rb').read()
undata = base64.b64decode(op1)
uncrypted = undata.decode()
skillinfo = json.loads(uncrypted)

op2 = open('src/data/skillinfo/charaOrb.json','r',encoding='utf-8')
charaOrb = json.load(op2)
chara_list = []
for chara in charaOrb:
    chara_list.append(chara)

def get_skill_set(chara,alt,rank,exceed):
    if alt == True:
        assetsid = charaOrb.get(chara).get('assetsid')
        p1tp = charaOrb.get(chara).get('p1')
        a1tp = charaOrb.get(chara).get('a1')
        s1tp = charaOrb.get(chara).get('s1')
        s2tp = charaOrb.get(chara).get('s2')
        s3tp = charaOrb.get(chara).get('s3')

    elif alt == False:
        assetsid = charaOrb.get(chara)[rank].get('assetsid')
        p1tp = charaOrb.get(chara)[rank].get('p1')
        a1tp = charaOrb.get(chara)[rank].get('a1')
        s1tp = charaOrb.get(chara)[rank].get('s1')
        s2tp = charaOrb.get(chara)[rank].get('s2')
        s3tp = charaOrb.get(chara)[rank].get('s3')

    else: pass

    if exceed == '1':
        p1nm = assetsid+'_r1_P1_name' 
        p1if = assetsid+'_r1_P1_skillinfo'
        a1nm = assetsid+'_r1_A1_name' 
        a1if = assetsid+'_r1_A1_skillinfo'
        s1nm = assetsid+'_r1_S1_name' 
        s1if = assetsid+'_r1_S1_skillinfo'
        s2nm = assetsid+'_r1_S2_name' 
        s2if = assetsid+'_r1_S2_skillinfo'
        s3nm = assetsid+'_r1_S3_name' 
        s3if = assetsid+'_r1_S3_skillinfo'

    elif exceed == '2':
        p1nm = assetsid+'_r2_P1_name' 
        p1if = assetsid+'_r2_P1_skillinfo'
        a1nm = assetsid+'_r2_A1_name' 
        a1if = assetsid+'_r2_A1_skillinfo'
        s1nm = assetsid+'_r2_S1_name' 
        s1if = assetsid+'_r2_S1_skillinfo'
        s2nm = assetsid+'_r2_S2_name' 
        s2if = assetsid+'_r2_S2_skillinfo'
        s3nm = assetsid+'_r2_S3_name' 
        s3if = assetsid+'_r2_S3_skillinfo'
    else:
        p1nm = assetsid+'_P1_name' 
        p1if = assetsid+'_P1_skillinfo'
        a1nm = assetsid+'_A1_name' 
        a1if = assetsid+'_A1_skillinfo'
        s1nm = assetsid+'_S1_name' 
        s1if = assetsid+'_S1_skillinfo'
        s2nm = assetsid+'_S2_name' 
        s2if = assetsid+'_S2_skillinfo'
        s3nm = assetsid+'_S3_name' 
        s3if = assetsid+'_S3_skillinfo'

    def info(item):
        skill = skillinfo.get(item)
        return skill

    P1 = f'⭐{p1tp}「{info(p1nm)}」\n{info(p1if)}'
    A1 = f'⭐{a1tp}「{info(a1nm)}」\n{info(a1if)}'
    S1 = f'⭐{s1tp}「{info(s1nm)}」\n{info(s1if)}'
    S2 = f'⭐{s2tp}「{info(s2nm)}」\n{info(s2if)}'
    S3 = f'⭐{s3tp}「{info(s3nm)}」\n{info(s3if)}'

    result = (P1,A1,S1,S2,S3)
    return result



@on_command('skillinfo',shell_like=True,aliases='技能组查询',only_to_me=False)
async def argv(session:CommandSession):
    if str(session.event.group_id) not in groupmsg_banlist:
        pass
    else:
        session.finish('管理员禁用了群聊功能,请私聊普吉机器人使用')
    argv_chara = session.argv[0]
    argv_rank = session.argv[1]
    try:
        argv_exceed = session.argv[2]
    except:
        argv_exceed = '0'

    fzwz = process.extractOne(argv_chara,chara_list)
    if fzwz[1] > 50:
        chara = fzwz[0]
    else:
        session.finish()

    if 'Alt' in chara:
        alt = True
    else: 
        alt = False
    
    if argv_rank in ['1','2','3']:
        rank = int(argv_rank)-1
    else:
        session.finish('格式错误,请输入数字后重试')
    
    if argv_exceed in ['0','1','2']:
        exceed = argv_exceed
    else:
        session.finish('格式错误,请输入数字后重试')

    result = get_skill_set(chara,alt,rank,exceed)
    await session.send('\n\n'.join(result))
