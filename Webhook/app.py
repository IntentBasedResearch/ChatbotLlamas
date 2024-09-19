import pandas as pd
from textgenie import TextGenie

#textgenie = TextGenie("ramsrigouthamg/t5_paraphraser",'bert-base-uncased')

x = pd.read_json("intents.json")
y = pd.read_csv("intents.intents.csv")

intent = []

for i in range(len(x["intents"])):
    #print(textgenie.augment_sent_t5(x["intents"][i]["text"],"paraphrase: "))
    intent.append([x["intents"][i]["text"],x["intents"][i]["nile"]])

'''
for j in range(len(y)):
    if y['text'][j]!="all" and y['text'][j]!="traffic" and y['text'][j]!="dorms" and y['text'][j]!="students" and y["text"][j]!="student" and y['text'][j]!="a student" and y['text'][j]!="for professors":
        v  = y['nile'][j]
        v = v.replace("buildIntent","uniIntent")
        intent.append([y['text'][j],v])
'''

intent.append(["Inspect packets for all students","define intent uniIntent: for group('students') add middlebox('dpi')"])
intent.append(['Inspect packets that come from gateway and go to the webserver',"define intent stnIntent: from endpoint('gateway') to endpoint('webserver') add middlebox('dpi')"])
x = pd.DataFrame(intent,columns=["text","nile"])

x.to_csv("Intent.csv",sep=";", index=False)