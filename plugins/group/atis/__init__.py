from nonebot import on_command,CommandSession
from nonebot import get_bot

import re
import requests
from nonebot import on_natural_language, NLPSession, IntentCommand

@on_natural_language(keywords={'ATIS-'},only_to_me=False)
async def atis_nlp(session: NLPSession):
    # 返回意图命令，前两个参数必填，分别表示置信度和意图命令名
    return IntentCommand(90.0, 'atis')

bot = get_bot()
@on_command("atis", only_to_me=False, aliases=('D-ATIS','ATIS','气象报文'))
async def atis(session: CommandSession):
    text = session.ctx["message"][0]["data"]["text"]
    await session.send('飞行气象情报/Aviation Meteorological Information')
    try:
        p = r'(?<=ATIS-).+'
        pattern = re.compile(p)
        matcher1 = re.search(pattern,text)
        icao = matcher1.group(0)
    except:
        icao = 'ZBAA'

    response = requests.get("http://report.qdatm.net/content.aspx?obcc=" + icao)

    #log.logger.debug(response.text)  #打印获取ATIS的response
    try:
        p = r'(?<=&nbsp;&nbsp; ).+?(?=<BR/>----)'
        pattern = re.compile(p, re.DOTALL)
        matcher1 = re.search(pattern,response.text)
        printtime = matcher1.group(0)
        printtime = printtime.replace("-------------------------------------------------------------------------------","")
        printtime = printtime.replace("<BR/>","\n")
        printtime = printtime.replace("\n\n","")
        await session.send(printtime)
    except:
        await session.send('ATIS获取失败')
