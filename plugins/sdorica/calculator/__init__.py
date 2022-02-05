# -*- coding:utf-8 -*-
# Author : Syaoran@sc33.top

from nonebot import on_command, CommandSession
from nonebot import get_bot
from nonebot import on_natural_language, NLPSession, IntentCommand

from fuzzywuzzy import process
import json

import yaml 

data = yaml.load(open('src/settings.yaml',encoding='utf-8'))
groupmsg_banlist = data.get('group').get('event').get('calculator').get('groupmsg_banlist')


charaList = []
base = json.load(open('src/data/calculator/base.json','r',encoding='utf-8'))
for key in base:
    charaList.append(key)


class standard:
    """对输入的参数进行标准化参数设置"""

    def __init__(self,chara,rank,level,exceed,charaList):
        self.ch = chara
        self.rk = rank
        self.lv = level
        self.ex = exceed
        self.ls = charaList

    def _charName(self):
        """角色名称,返回元组，形如：(角色，匹配度)"""
        charName = process.extractOne(self.ch,self.ls)
        return charName

    def _charRank(self):
        """共鸣阶级"""
        if self.rk not in ['0','1','2','3']:
            if (self.rk == '三阶'or self.rk == '金色'):
                charRank = 3
            elif (self.rk == '二阶'or self.rk == '紫色'):
                charRank = 2
            elif (self.rk == '一阶'or self.rk == '蓝色'):
                charRank = 1
            elif (self.rk == '零阶'or self.rk == '白色'):
                charRank = 0
        else: charRank = int(self.rk)

        return charRank

    def _charLevel(self):
        """角色等级"""
        charLevel = int(self.lv)
        return charLevel

    def _charExceed(self):
        """角色加值"""
        charExceed = int(self.ex)
        return charExceed

    def standardize(self):
        """执行标准化方法"""
        charName = standard._charName(self)
        charRank = standard._charRank(self)
        charLevel = standard._charLevel(self)
        charExceed = standard._charExceed(self)

        return charName,charRank,charLevel,charExceed



class charCulator():
    """角色加值计算器"""

    _base_ratio = 1.06
    _health_exceedRatio = 1.03
    
    def __init__(self,good,base):
        """数值初始化"""
        ch_fwzy,self.rk,self.lv,self.ex = good
        self.ch = ch_fwzy[0]
        self.atk = base.get(self.ch).get('baseAtk')
        self.hp = base.get(self.ch).get('baseHp')

    def _rankRatio(self):
        """共鸣阶级加成倍率"""
        if self.rk == 0 :
            rankRatio = 1
        elif self.rk == 1:
            rankRatio = 1.08
        elif self.rk == 2:
            rankRatio = 1.2
        elif self.rk == 3:
            rankRatio = 1.35

        return rankRatio

    def _exceedRatio(self):
        """加值加成倍率"""
        if (self.ex >= 0 and self.ex <= 5) :
            exceedRatio = 1.02 ** self.ex
        elif (self.ex > 5 and self.ex <= 10):
            exceedRatio = 1.02**5 * 1.025**(self.ex-5)
        elif (self.ex > 10 and self.ex <= 15):
            exceedRatio = 1.02**5 * 1.025**5 * 1.035 **(self.ex-10)

        return exceedRatio

    def charCulate(self):
        """加值计算"""
        rankRatio = charCulator._rankRatio(self)
        exceedRatio = charCulator._exceedRatio(self)
        charAtk = charCulator._base_ratio **(self.lv-1) * self.atk * rankRatio * exceedRatio
        charHp = charCulator._base_ratio **(self.lv-1) * self.hp * rankRatio *  charCulator._health_exceedRatio ** self.ex

        charResult = (charAtk,charHp)
        return charResult


@on_natural_language(keywords={'加值计算','加值查询','角色加值'},only_to_me=False)
async def calculator_nlp(session: NLPSession):
    return IntentCommand(70.0, 'calculator')

bot = get_bot()
@on_command("calculator", only_to_me=False, aliases=('加值计算器'))
async def calculator(session: CommandSession):
    if str(session.event.group_id) not in groupmsg_banlist:
        pass
    else:
        session.finish('管理员禁止了群聊使用，请私聊普吉机器人')

    if len(session.event["message"][0]["data"]["text"]) > 6:
        session.finish()
    else:
        pass
        
    while session.current_arg_text == '退出':
        session.finish()

    chara_ssn = session.get('chara',prompt='请问你想查询哪位角色？(支持模糊识别。可使用"退出"终止对话)')
    chara_ssns = chara_ssn.replace(' ','')
    chara = process.extractOne(chara_ssns,charaList)[0]
        
    rank = session.get('rank',prompt='请输入{}的共鸣阶级，例如：3、三阶或金色'.format(chara))
    level = session.get('level',prompt='请输入需要查询角色的等级,数字格式:0~70')
    exceed = session.get('exceed',prompt='请输入需要查询角色的加值数,数字格式:0~15')

    try:
        good = standard(chara,rank,level,exceed,charaList).standardize()
        charResult = charCulator(good,base).charCulate()

        result_ln1 = chara+'加值情况：'
        result_ln2 = '⚔攻击：'+str(int(charResult[0]))
        result_ln3 = '❤血量：'+str(int(charResult[1]))

        result = '\n'.join((result_ln1,result_ln2,result_ln3))

        await session.send(result)

    except:
        await session.send('输入格式错误,请按照提示重试')