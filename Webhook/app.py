import pandas as pd

x = pd.read_json("intents.json")

intent = []

for i in range(len(x["intents"])):

    intent.append([x["intents"][i]["text"],x["intents"][i]["nile"]])


x = pd.DataFrame(intent,columns=["text","nile"])

x.to_csv("Intent.csv",sep=";", index=False)