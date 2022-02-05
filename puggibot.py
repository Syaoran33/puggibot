import nonebot
import config

from nonebot.log import logging
from time import localtime

# logging

date = localtime()
logger_file = 'logs/{}-{}-{}.log'.format(date[0], date[1], date[2])

handler = logging.handlers.TimedRotatingFileHandler(
    filename=logger_file, when='D', interval=1)
handler.suffix = "logs/%Y-%m-%d.log"
logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s] - %(levelname)s: %(message)s',
                    handlers=[handler]
                    )

if __name__ == '__main__':
    nonebot.init(config)
    nonebot.load_plugins("plugins/sdorica","plugins.sdorica")
    nonebot.load_plugins("plugins/group","plugins.group")
    nonebot.load_plugins("plugins/setu","plugins.setu")
    nonebot.load_plugins("plugins/social","plugins.social")
    nonebot.load_plugins("plugins/syaoran","plugins.syaoran")
    #nonebot.load_plugins("plugins/sdorica_api","plugins.sdorica_api")
    nonebot.run()
