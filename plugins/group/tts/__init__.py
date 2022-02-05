# -*- coding: utf-8 -*-
# Author: Syaoran
# Plugin: TTS
# LastUpdate: 3rd,Dec,2020

from nonebot import on_command,CommandSession

import requests
import json

@on_command('speak_tts_tecent',only_to_me=False,aliases='给爷说',shell_like=True)
async def speak_tts_tecent(session:CommandSession):
    try:
        text = session.argv[0]
    except:
        await session.finish('未知的格式错误,删除符号试试')

    cq_text = f'[CQ:tts,text={text}]'
    await session.send(cq_text)


#FOR BAIDU TTS
#PARM ABSTRACT TAG
#0 标准女声
#1/2标准男声
#3 情感男生 大叔，绅士
#4 度丫丫 女孩
#5 度小娇 女声
#6 朗读男声 诗人
#8 播音男声 年轻
#9 播音男声 老陈
#100 标准女声
#102/103 度米朵 萝莉
#106 度博文 播音
#110 度小童 正太
#111 度小萌

@on_command('speak_tts_baidu_LOLITA',only_to_me=False,aliases='萝莉说',shell_like=True)
async def speak_tts_baidu_LOLITA(session:CommandSession):
    try:
        text = session.argv[0]
    except:
        await session.finish('未知的格式错误,删除符号试试')

    url = f'https://tts.baidu.com/text2audio?tex={text}&cuid=baike&lan=ZH&ctp=1&pdt=301&vol=9&rate=32&per=103'
    cq_text = f'[CQ:record,file={url}]'
    await session.send(cq_text)


@on_command('speak_tts_baidu_YAYA',only_to_me=False,aliases=('丫丫说','女儿说'),shell_like=True)
async def speak_tts_baidu_YAYA(session:CommandSession):
    try:
        text = session.argv[0]
    except:
        await session.finish('未知的格式错误,删除符号试试')

    url = f'https://tts.baidu.com/text2audio?tex={text}&cuid=baike&lan=ZH&ctp=1&pdt=301&vol=9&rate=32&per=4'
    cq_text = f'[CQ:record,file={url}]'
    await session.send(cq_text)

@on_command('speak_tts_baidu_CHARM',only_to_me=False,aliases='御姐说',shell_like=True)
async def speak_tts_baidu_CHARM(session:CommandSession):
    try:
        text = session.argv[0]
    except:
        await session.finish('未知的格式错误,删除符号试试')

    url = f'https://tts.baidu.com/text2audio?tex={text}&cuid=baike&lan=ZH&ctp=1&pdt=301&vol=9&rate=32&per=5'
    cq_text = f'[CQ:record,file={url}]'
    await session.send(cq_text)

@on_command('speak_tts_baidu_SYOUJYO',only_to_me=False,aliases=('少女说','妹妹说'),shell_like=True)
async def speak_tts_baidu_SYOUJYO(session:CommandSession):
    try:
        text = session.argv[0]
    except:
        await session.finish('未知的格式错误,删除符号试试')

    url = f'https://tts.baidu.com/text2audio?tex={text}&cuid=baike&lan=ZH&ctp=1&pdt=301&vol=9&rate=32&per=111'
    cq_text = f'[CQ:record,file={url}]'
    await session.send(cq_text)


@on_command('speak_tts_baidu_TOSHISHITANO_ODOKONOKO',only_to_me=False,aliases=('正太说','男孩说'),shell_like=True)
async def speak_tts_baidu_TOSHISHITANO_ODOKONOKO(session:CommandSession):
    try:
        text = session.argv[0]
    except:
        await session.finish('未知的格式错误,删除符号试试')

    url = f'https://tts.baidu.com/text2audio?tex={text}&cuid=baike&lan=ZH&ctp=1&pdt=301&vol=9&rate=32&per=110'
    cq_text = f'[CQ:record,file={url}]'
    await session.send(cq_text)


@on_command('speak_tts_baidu_GEPING',only_to_me=False,aliases=('葛平说','葛炮说'),shell_like=True)
async def speak_tts_baidu_GEPING(session:CommandSession):
    try:
        text = session.argv[0]
    except:
        await session.finish('未知的格式错误,删除符号试试')

    url = f'https://tts.baidu.com/text2audio?tex={text}&cuid=baike&lan=ZH&ctp=1&pdt=301&vol=9&rate=32&per=8'
    cq_text = f'[CQ:record,file={url}]'
    await session.send(cq_text)

@on_command('speak_tts_baidu_GENTLEMAN',only_to_me=False,aliases=('大叔说','绅士说'),shell_like=True)
async def speak_tts_baidu_GENTLEMAN(session:CommandSession):
    try:
        text = session.argv[0]
    except:
        await session.finish('未知的格式错误,删除符号试试')

    url = f'https://tts.baidu.com/text2audio?tex={text}&cuid=baike&lan=ZH&ctp=1&pdt=301&vol=9&rate=32&per=3'
    cq_text = f'[CQ:record,file={url}]'
    await session.send(cq_text)

@on_command('speak_tts_baidu_ANNONCER',only_to_me=False,aliases='播音说',shell_like=True)
async def speak_tts_baidu_ANNONCER(session:CommandSession):
    try:
        text = session.argv[0]
    except:
        await session.finish('未知的格式错误,删除符号试试')

    url = f'https://tts.baidu.com/text2audio?tex={text}&cuid=baike&lan=ZH&ctp=1&pdt=301&vol=9&rate=32&per=9'
    cq_text = f'[CQ:record,file={url}]'
    await session.send(cq_text)

@on_command('speak_tts_baidu_POET',only_to_me=False,aliases=('朗读说','诗人说'),shell_like=True)
async def speak_tts_baidu_POET(session:CommandSession):
    try:
        text = session.argv[0]
    except:
        await session.finish('未知的格式错误,删除符号试试')

    url = f'https://tts.baidu.com/text2audio?tex={text}&cuid=baike&lan=ZH&ctp=1&pdt=301&vol=9&rate=32&per=6'
    cq_text = f'[CQ:record,file={url}]'
    await session.send(cq_text)


#Japanese Ver TTS
def speak_tts_jp_ttsmp3(msg,speaker):

    headers = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'Content-type': 'application/x-www-form-urlencoded',
        'Accept': '*/*',
        'Origin': 'https://ttsmp3.com',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://ttsmp3.com/text-to-speech/Japanese/',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

    data = {
    'msg': msg, #'わたし、気になります！'
    #'lang': 'Takumi',
    'lang': speaker, #Mizuki
    'source': 'ttsmp3'
    }

    response = requests.post('https://ttsmp3.com/makemp3_new.php', headers=headers,data=data)

    data = json.loads(response.text)
    url = data.get('URL')
    return url


@on_command('speak_tts_jp1_MIZUKI',only_to_me=False,aliases=('日语说','霓虹说'),shell_like=True)
async def speak_tts_jp1_MIZUKI(session:CommandSession):
    try:
        text = session.argv[0]
    except:
        await session.finish('未知的格式错误,删除符号试试')

    url = speak_tts_jp_ttsmp3(text,'Mizuki')
    cq_text = f'[CQ:record,file={url}]'
    await session.send(cq_text)