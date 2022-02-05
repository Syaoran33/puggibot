from nonebot import on_command,CommandSession
import nonebot

'''
import yaml

data = yaml.load(open('src/settings.yaml',encoding='utf-8'))
reminder_list = data.get('group').get('event').get('wonderland').get('reminder_list')
'''

import json
import random


def quest():
    data = json.load(open('src/data/question/bank.json','r',encoding='utf-8'))
    one = random.randrange(len(data))
    qust = data[str(one+1)]

    author = qust['auth']
    title = qust['titl']
    opta = qust['A']
    optb = qust['B']
    optc = qust['C']
    optd = qust['D']
    answer = qust['aws']
    note = qust['note']

    text1 = f'{str(one+1)}.{title}\nA.{opta}\nB.{optb}\nC.{optc}\nD.{optd}'
    text2 = f'感谢本题作者：{author}\n正确答案是：{answer}\n解析/备注：\n{note}'

    return answer,text1,text2

def quest_add(author,title,opta,optb,optc,optd,aws,note): 
    data = json.load(open('src/data/question/bank.json','r',encoding='utf-8'))
    idx = len(data)
    dt = {
        str(idx+1):{
            'type': 'sgl',
            'auth':str(author),
            'titl': str(title),
            'A': str(opta),
            'B': str(optb),
            'C': str(optc),
            'D': str(optd),
            'aws': str(aws),
            'note': str(note)
        }
    }
    data.update(dt)
    with open('src/data/question/bank.json','w',encoding='utf-8') as f:
        f.write(json.dumps(data,ensure_ascii=False))
        f.close()


@on_command('questionbank',aliases=('万象题库','万象物语题库'),only_to_me=False)
async def questionbank(session: CommandSession):

    while session.current_arg_text == '退出':
        session.finish()

    if session.current_arg == '':
        global answer,text2
        answer,text1,text2 = quest()
        await session.send(text1)

    answer_ipt = session.get('answer',prompt='请输入答案(字母选项)')
    answer_usr = answer_ipt.strip().upper().replace(' ','')

    if answer_usr == answer:
        await session.send('噗噗噗，回答正确！\n'+text2)
    else:
        await session.send('感觉哪里怪怪的!\n'+text2)


@on_command('questionbank_add',aliases=('万象题库添加','万象物语题库添加'),only_to_me=False)
async def questionbank_add(session: CommandSession):

    while session.current_arg_text == '退出':
        session.finish()


    author_ipt = str(session.get('author',prompt='请输入您的尊姓大名或作者名称'))
    title_ipt = str(session.get('title',prompt='请输入题目信息,现仅支持四个选项的单选'))
    
    opta_ipt = str(session.get('opta',prompt='请输入选项A的内容'))
    optb_ipt = str(session.get('optb',prompt='请输入选项B的内容'))
    optc_ipt = str(session.get('optc',prompt='请输入选项C的内容'))
    optd_ipt = str(session.get('optd',prompt='请输入选项D的内容'))

    aws_ipt = str(session.get('aws',prompt='请输入题目答案,请输入大写字母'))
    if aws_ipt[0].upper() not in ['A','B','C','D']:
        session.finish('会话结束，错误的答案格式')

    note_ipt = session.get('note',prompt='请输入本题的解析或备注')

    quest_add(author_ipt,title_ipt,opta_ipt,optb_ipt,optc_ipt,optd_ipt,aws_ipt,note_ipt)
    await session.send('噗噗噗~感谢您提供的题目,已经收录在题库中了')