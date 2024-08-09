import pandas as pd
import ast

df = pd.read_csv("Intent.csv",sep=";")


text_vectors = []
for _, row in df.iterrows():
    text = row["text"]
    nile = row["nile"]
    

    
 
df.reset_index(drop=True, inplace=True)

df.to_csv("processed_intent.csv", index=False)