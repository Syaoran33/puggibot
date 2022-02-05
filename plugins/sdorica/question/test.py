import json
import random


def quest():
    data = json.load(open('new.json','r',encoding='utf-8'))
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
    data = json.load(open('new.json','r',encoding='utf-8'))
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
    with open('new.json','w',encoding='utf-8') as f:
        f.write(json.dumps(data,ensure_ascii=False))
        f.close()
