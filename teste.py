import ollama
import pandas as pd

dataset = pd.read_csv("processed_intent.csv")

matched_intent = dataset['text']

response = dataset['nile']

modelfile=f'''
FROM llama3
SYSTEM  You have to contruct a responsed based in intents.this intent: {matched_intent} construct this response: {response}. 

'''

ollama.create(model='example3', modelfile=modelfile)