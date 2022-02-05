# -*- coding:utf-8 -*-
# Author:Syaoran@sc33.top
# Plugin: Prononce
# LastUpdate: 28th,Nov,2020

from nonebot import get_bot
from nonebot import scheduler
import json
import requests
import time

import yaml 
ym = yaml.load(open('src/settings.yaml',encoding='utf-8'))
pronounce_list = ym.get('group').get('event').get('prononce').get('prononce_list')

class deposit:
    """游戏公告寄存器"""

    url = 'https://1x0x0-api-sermo.rayark.net/v1/sdorica-game/news?locale=zh_CN'
    deposit_list = []

    def remove(self):
        del self.deposit_list[0]

    def spider(self):
        """获取公告长度"""
        res = requests.get(self.url)
        data = json.loads(res.text)
        lenth = len(data)
        self.deposit_list.append(lenth)


    def judge(self):
        """判断更新"""
        if self.deposit_list[0] != self.deposit_list[1]:
            return True
        else:
            return False

    def depositor(self):
        deposit.spider(self)
        judgement = deposit.judge(self)
        deposit.remove(self)
        return judgement

bot = get_bot()
depo = deposit()
depo.spider()
print('[Info]:Plugin_Sdorica_Prononce initial request!')

@scheduler.scheduled_job('interval', minutes=10)
async def pronounce():
    judgement = depo.depositor()

    def get_anno():
        url = 'https://exp-sermo-sdorica.dragonest.com/v1/sdorica-game/news?locale=zh_CN'
        res = requests.get(url)
        data = json.loads(res.text)[0]
        title= data.get('title')
        content = data.get('content')
        text = title + '\n'+content
        return text 

    while judgement:
        try:
            text = get_anno()
            for group_id in pronounce_list:
                await bot.send_group_msg(group_id=group_id, message=text)
            break
        except :pass

