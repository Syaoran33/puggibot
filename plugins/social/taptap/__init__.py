# -*- coding:utf-8 -*-
# Author: Syaoran
# Plugin: Wonderland Homeworks
# LastUpdate: 6th,Nov,2020


from nonebot import on_command,CommandSession

import requests
import json

requests.urllib3.disable_warnings()


class taptap_api_v1:
    """描述：taptap数据接口api"""
    headers = {
        'Host': 'api.taptapdada.com',
        'User-Agent': 'okhttp/3.6.0',
    }
    

    def publish_topic(self,uid:str,limit:str):
        """描述：用户发贴数据,默认从0开始显示10条,不含游戏评价"""
        params = {
            'action':'publish_topic',
            'user_id': uid,
            'limit':limit,
            #'from': '0'
            'X-UA': 'V=1&PN=TapTap&VN_CODE=517&LOC=CN&LANG=zh_CN&CH=default&UID=36d85b58-9f06-4e18-a94b-6caa26defb7a'
        }


        response = requests.get('https://api.taptapdada.com/feed/v1/by-user', headers=self.headers, params=params)

        response.encoding = response.apparent_encoding
        metadata = json.loads(response.text)

        return metadata


api = taptap_api_v1()

from fuzzywuzzy import process
import time

def get_uid(name_ipt):
    data = json.load(open('users/plugins/taptap/hjworks/uid.json','r',encoding='utf-8'))
    name_ls = []
    for name in data:
        name_ls.append(name)
    fzwz = process.extractOne(name_ipt,name_ls)
    if fzwz[1] < 50:
        return False
    
    uid = data[fzwz[0]]

    return uid

@on_command('hjworks',only_to_me=False,aliases=('幻境作业查询','康康作业','幻境作业gkd'))
async def hjworks(session:CommandSession):
    
    while session.current_arg_text == '退出':
        session.finish()

    
    name_ipt = session.get('name',prompt='请问你想查询哪位大佬的作业？\n(仅限taptap幻境版块,支持模糊识别。使用[退出]强制退出会话)')

    
    uid = get_uid(name_ipt)
    if uid == False:
        session.finish('未查询到或暂未收录,可以使用命令[幻境作业添加]添加哦~')

    try:
        metadata = api.publish_topic(uid,'10')
        data_list = metadata.get('data').get('list')
    except:
        session.finish('请求对应taptapid错误,请重试')

    text_list = []
    cq_text_list = []
    for i in range(len(data_list)):
        data = data_list[i]
        created_time = data.get('created_time')
        local_time = time.localtime(created_time)
        time_st = time.strftime("[%m-%d]",local_time)
        topic_url = 'https://www.taptap.com/topic/'+str(data.get('id'))[6:]
        title = data.get('title').split('</b>')[1].replace('&nbsp;','')
        try:
            content_text = data.get('content_text')
            content = "".join(content_text.split())
        except:
            content = "普吉机器人未识别到文本信息，推测可能是视频"
        try:
            medium_url = data.get('content_obj').get('data')[0].get('medium_url')
            if medium_url == None:
                medium_url = 'https://gitee.com/sdorica/puggibot/raw/master/src/images/plugins/poke/puggi_poke.jpg'
        except:
            medium_url = 'https://gitee.com/sdorica/puggibot/raw/master/src/images/plugins/poke/puggi_poke.jpg'
        text = f'{str(i+1)}.{time_st}{title}'
        #text = f'{i+1}.{title}()'
        #cq_text = f'[CQ:share, url={topic_url}, title={title}, content={content}, image={medium_url}]'.replace(' ','').replace('&','&amp;')

        xml = f"""<?xml version=\'1.0\' encoding=\'UTF-8\' standalone=\'yes\' ?>
        <msg serviceID="1" templateID="-1" action="web" brief="普吉机器人幻境作业" sourceMsgId="0" url="{topic_url}" flag="0" adverSign="0" multiMsgFlag="0">
            <item layout="2" advertiser_id="0" aid="0">
                <picture cover="{medium_url}" w="0" h="0" />
                <title>{title}</title>
                <summary>{content}</summary>
            </item>
            <source name="TapTap 发现好游戏" icon="https://assets.tapimg.com/web-app/favicon.ico" action="" appid="0" />
        </msg>
        """
        cq_text = f'[CQ:xml,data={xml}]'.replace('&','&amp;')
        text_list.append(str(text))
        cq_text_list.append(cq_text)
    
    text_result = '\n'.join(text_list)
    if session.current_key == 'name':
        await session.send(text_result)

    no_ipt = session.get('no',prompt='请输入对应的序号(数字格式)以获取链接,或使用[退出]强制结束会话;\n如果未返回发帖列表,请私聊普吉使用,该问题将在后续版本解决')

    try:
        no = int(no_ipt.strip())
    except:
        session.finish('输入了错误的数字序号')

    try:
        cq_text_result = cq_text_list[no-1]
    except:
        session.finish('超出数字范围')
    await session.send(cq_text_result)


@on_command('hjworks_addition',only_to_me=False,aliases=('幻境作业-添加用户','幻境作业添加','幻境作业更新'),shell_like=True)
async def hjworks_addition(session:CommandSession):
    def uid_addition(uid,name):
        data = json.load(open('users/plugins/taptap/hjworks/uid.json','r',encoding='utf-8'))
        item = {
            name:str(uid)
        }
        data.update(item)

        export = json.dumps(data,ensure_ascii=False)

        f = open('users/plugins/taptap/hjworks/uid.json','w',encoding='utf-8')
        f.write(export)
        f.close()

        return True

    try:
        name_ipt = str(session.argv[0]).strip()
    except:
        await session.finish('格式错误，参考:\n幻境作业-添加 小狼 123456')

    try:
        uid_ipt = int(session.argv[1])
    except:
        await session.finish('格式错误，参考:\n幻境作业-添加 小狼 123456')

    
    name = name_ipt
    uid = uid_ipt

    if uid_addition(uid,name):
        await session.send(f'添加成功,试试查询{name}的作业吧!')
    else:
        await session.finish('数据库异常')