from nonebot import on_command,CommandSession

from PIL import Image,ImageOps,ImageDraw,ImageFont
from cv2 import cv2
from io import BytesIO
import numpy as np
import requests
import time
import os

import yaml

data = yaml.load(open('src/settings.yaml',encoding='utf-8'))
groupmsg_banlist = data.get('group').get('event').get('charchef').get('groupmsg_banlist')

mask = 'src/data/charchef/material/mask.png'
bg = 'src/data/charchef/material/floor.png'
new_frame = 'src/data/charchef/frame/new.png'



def charChef(url,text,rank,fontsize,offsetXaxis,offsetYaxis,new,convert):
    
    res = requests.get(url)
    img = Image.open(BytesIO(res.content))
    img = img.convert('RGBA')
    img = cv2.cvtColor(np.asarray(img),cv2.COLOR_RGB2BGR)
    a,b = img.shape[0:2]
    fb = float(298/b)
    fa = float(427/a)
    img = cv2.resize(img, (0, 0), fx=fa, fy=fb, interpolation=cv2.INTER_NEAREST)
    img = cv2.resize(img, (179, 256), interpolation=cv2.INTER_CUBIC)
    
    mask1 = cv2.imread(mask,cv2.IMREAD_GRAYSCALE)
    img = cv2.add(img, np.zeros(np.shape(img), dtype=np.uint8), mask=mask1)

    def transparent_back(img):
        img = img.convert('RGBA')
        L, H = img.size
        color_0 = (255, 255, 255, 255)  
        for h in range(H):
            for l in range(L):
                dot = (l, h)
                color_1 = img.getpixel(dot)
                if color_1 == color_0:
                    color_1 = color_1[:-1] + (0,)
                    img.putpixel(dot, color_1)
        return img

    mask2 = cv2.imread(mask)
    mask2= cv2.bitwise_not(mask2)

    img = cv2.add(img, mask2)
    img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)) 
    img = transparent_back(img)
    
    bcg = Image.open(bg)
    bcg.paste(img,img)
    img = bcg
    img =ImageOps.expand(img, (59,85,59,85)) 
    img = img.resize((298,427))

    rank = int(rank)
    if rank == 2:
        frame = 'src/data/charchef/frame/frame1.png'
    elif rank == 3:
        frame = 'src/data/charchef/frame/frame5.png'
    elif rank == 4:
        frame = 'src/data/charchef/frame/frame20.png'
    elif rank == 5 :
        frame= 'src/data/charchef/frame/frame50.png'
    else :
        pass

    frame = Image.open(frame)
    img.paste(frame,frame)


    def text_border(draw, x, y, font, shadowcolor, fillcolor):
        # thin border
        draw.text((x - 1, y), text, font=font, fill=shadowcolor)
        draw.text((x + 1, y), text, font=font, fill=shadowcolor)
        draw.text((x, y - 1), text, font=font, fill=shadowcolor)
        draw.text((x, y + 1), text, font=font, fill=shadowcolor)
        
        # thicker border
        draw.text((x - 1, y - 1), text, font=font, fill=shadowcolor)
        draw.text((x + 1, y - 1), text, font=font, fill=shadowcolor)
        draw.text((x - 1, y + 1), text, font=font, fill=shadowcolor)
        draw.text((x + 1, y + 1), text, font=font, fill=shadowcolor)
        
        # now draw the text over it
        draw.text((x, y), text, font=font, fill=fillcolor)
        

    #字体配置
    pointsize = int(fontsize)
    fillcolor = (255,255,255)
    shadowcolor = "black"
    font="src/data/charchef/font/Main_NotoSansCJKjp-Bold.otf"


    def calcu_len(text):
        length = 0
        for uchar in text:
            if uchar >= u'\u4e00' and uchar<=u'\u9fa5':
                length = length + 2
            else:
                length = length + 1
            
        return length
    length = calcu_len(text)
    text_len = length * pointsize / 2
        

    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font, pointsize)

    x_stand = 148 - text_len/2
    y_stand = 88
    x = x_stand + int(offsetXaxis)
    y=  y_stand + int(offsetYaxis)
    text_border(draw,x,y,font,shadowcolor,fillcolor)

    if new==True:
        frame_new = Image.open(new_frame) 
        img.paste(frame_new,frame_new)
    else: pass

    #for windows
    #pic_path = '\\src\\data\\charchef\\cache\\' + str(round(time.time(),2)) + '.png'
    
    #for linux
    pic_path = '/src/data/charchef/cache/' + str(round(time.time(),2)) + '.png'

    full_path = os.getcwd() + pic_path

    if convert:
        whtbg = Image.new("RGB",img.size,(255,255,255))
        whtbg.paste(img,img)
        img= whtbg
        img.save(full_path,quality=100)
    else:
        img.save(full_path,quality=100)

    return full_path


@on_command('charchef',only_to_me=False,aliases=('赋魂图生成','水图生成器'))
async def charchef(session: CommandSession):
    if str(session.event.group_id) not in groupmsg_banlist:
        pass
    else:
        session.finish('管理员禁止了群聊使用，请私聊普吉机器人')

    while session.current_arg_text == '退出':
        session.finish()

    pic = session.get('pic',prompt='请发送一张需要处理的图片,可使用"退出"强制结束会话')
    url = pic.split('url=',1)[1].split(']',1)[0]
    if 'http' in url:
        pass
    else:
        session.finish('会话结束,未成功收到图片')
    
    text = session.get('text',prompt='请输入标题(名称)').strip()
    if len(text) > 10:
        await session.finish('会话结束,您输入字符过长,限制10个字符')

    rank_ag = session.get('rank',prompt='请输入角色框颜色(金紫蓝灰)')
    if '金' in rank_ag:
        rank = '5'
    elif '紫' in rank_ag:
        rank = '4'
    elif '蓝' in rank_ag:
        rank = '3'
    elif '灰' in rank_ag:
        rank = '2'
    else:
        await session.finish('会话结束,您输入错误的角色框颜色')

    ft_ag = session.get('font',prompt='请输入字体大小,默认为24,或输入其他非数字字符跳过')
    try:
        fontsize = int(ft_ag)
        if (fontsize > 32) or (fontsize <= 0):
            await session.finish('会话结束，错误的字体大小')
    except:
        fontsize = 24

    new_ag = session.get('new',prompt='是否添加new标识(是/否)').strip()
    if new_ag == '是':
        new = True
    elif new_ag == '否':
        new = False
    else:
        await session.finish('会话结束,请输入是或否')

    cvt_ag = session.get('convert',prompt='默认为PNG透明图,是否转换为JPEG图(是/否)').strip()
    if cvt_ag == '是':
        convert = True
    elif cvt_ag == '否':
        convert = False
    else:
        await session.finish('会话结束,请输入是或否')
    
    full_path = charChef(url,text,rank,fontsize,0,0,new,convert)
    cq_text = f'[CQ:image,file=file:///{full_path}]'

    await session.send(cq_text)