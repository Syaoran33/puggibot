import pandas as pd 
import json

df = pd.DataFrame(pd.read_excel('bank.xlsx'))

values = df.values

null = {}
for i in range(len(values)):
    data = values[i]
    idx = data[0]
    tp = data[1]
    author = data[2]
    title = data[3]
    opta = data[4]
    optb = data[5]
    optc = data[6]
    optd = data[7]
    aws = data[8]
    note = data[9]


    dt ={
        str(idx):{
            'type':str(tp),
            'auth':str(author),
            'titl':str(title),
            'A':str(opta),
            'B':str(optb),
            'C':str(optc),
            'D':str(optd),
            'aws':str(aws),
            'note':str(note)
        }
    }
    null.update(dt)

with open('new.json','w',encoding='utf-8') as f:
    f.write(json.dumps(null,ensure_ascii=False))
    f.close()