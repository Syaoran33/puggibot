# -*- coding: utf-8 -*-
# Author: Syaoran
# Plugin: Help
# LastUpdate: 27th,Nov,2020


from nonebot import get_bot
from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand

import yaml
import re

data = yaml.load(open('src/data/help/helpbook.yaml',encoding='utf-8'))
menu = data.get('menu')
help_book = data.get('help')
title = menu.get('title')
ver = menu.get('ver')
func = menu.get('func')
link = menu.get('link')
menu_text = (title,ver,func,link)
menu_result = '\n'.join(menu_text)

bot = get_bot()
@on_command("menubook",only_to_me=False,aliases=('帮助','菜单'))
async def menubook(session: CommandSession):
    await session.send(menu_result)


@on_natural_language(keywords={'帮助-'},only_to_me=False)
async def nlp_help(session: NLPSession):
    return IntentCommand(90.0, 'get_help')

@on_command("get_help", only_to_me=False)
async def get_help(session: CommandSession):
    try:
        text = session.ctx["message"][0]["data"]["text"]
        p = r'(?<=帮助-).+'
        pattern = re.compile(p)
        matcher1 = re.search(pattern,text)
        num = int(matcher1.group(0)) -1
        name = help_book.get('help_list')[num]
        text = help_book.get(name)

        await session.send(text)
    except:
        await session.finish('请输入正确的的序号后重试')