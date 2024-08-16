import pandas as pd
from textgenie import TextGenie

textgenie = TextGenie("ramsrigouthamg/t5_paraphraser",'bert-base-uncased')

x = pd.read_json("intents.json")

intent = []

for i in range(len(x["intents"])):
    print(textgenie.augment_sent_t5(x["intents"][i]["text"],"paraphrase: "))
    intent.append([x["intents"][i]["text"],x["intents"][i]["nile"]])

intent.append(["Inspect packets for all students","define intent uniIntent: for group('students') add middlebox('dpi')"])
x = pd.DataFrame(intent,columns=["text","nile"])

x.to_csv("Intent.csv",sep=";", index=False)