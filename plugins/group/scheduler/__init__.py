# -*- coding:utf-8
# Author: Syaoran@sc33.top
# Plugins name : scheduler
# LastUpdate: 27th,Nov,2020

import nonebot
from nonebot import get_bot

import json
import requests
import time

import yaml

data = yaml.load(open('src/settings.yaml',encoding='utf-8'))
groupid_list = data.get('group').get('common_groupid_list')
reminder_list = data.get('group').get('event').get('wonderland').get('reminder_list')

reminder = data.get('wonderland').get('reminder')

message = reminder.get('message')
scheduler_day = reminder.get('scheduler_day')
scheduler_time = reminder.get('scheduler_time')
all_group = reminder.get('all_group')


#幻境提醒
bot = nonebot.get_bot()
@nonebot.scheduler.scheduled_job('cron', day_of_week =scheduler_day,hour=scheduler_time)
async def hjreminder():
    if all_group == True:
        for group_id in groupid_list:
            await bot.send_group_msg(group_id=group_id,message=message)
    else:
        for group_id in reminder_list:
            await bot.send_group_msg(group_id=group_id,message=message)