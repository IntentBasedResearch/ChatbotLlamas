import logging
import ollama
import os
import requests
import json
import pandas as pd


from qdrant_client import QdrantClient
from qdrant_client.models import CollectionDescription, Distance, VectorParams



# Define a function to search for the closest intent based on user input
def search_intent(user_input, cont):
    user_vector = ollama_client.embeddings(model="example", prompt=user_input)["embedding"]
    results = client.search(collection_name="intentEval_db", query_vector=user_vector, limit=1)
    print(user_input)
 
    if results:
        best_match: ScoredPoint = results[0]
        print(best_match.score)
        
        if best_match.score >= 0.90:
            best_match_id = best_match.id
           
            matched_intent = z.iloc[best_match_id]["text"]
            response = z.iloc[best_match_id]["nile"]
           
            xxx = dataset[dataset['text']==user_input]
           
            if xxx['nile'].iloc[0] == response:
                cont+=1
            
                return cont
            else:
                return cont
        else:
            best_match_id = best_match.id
            matched_intent = z.iloc[best_match_id]["text"]
            response = z.iloc[best_match_id]["nile"]
          
            output= ollama.generate(
  model="example",
  prompt=f"this intent: {matched_intent} construct this response: {response}. What this intent: {user_input} construct response?.Response Only unitIntent"
)
            ttt = output['response']
           
            if ttt.rfind('uniIntent:'):
                response2= ttt[ttt.rfind('uniIntent:'): ]
                response2 = "define intent " + response
                print(response2)
                response = dataset[dataset['text']==user_input]
                if response2 == response['nile'].iloc[0]:
                    cont+=1
                   
                    return cont
            else:
                return cont


    return cont        
          
    
    


client = QdrantClient(host="127.0.0.1", port=6333)
ollama_client = ollama.Client("http://127.0.0.1:11434")
dataset = pd.read_csv("processed_intent.csv")
x = pd.read_csv("processed_alpha.csv",sep=";")

z = dataset.sample(frac=0.10)
z.reset_index(drop=True, inplace=True)



# Define collection schema
collection_name = "intentEval_db"
client.recreate_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(size=4096, distance=Distance.COSINE),
)

# Prepare and index data
for index, row in z.iterrows():
    vector = ollama_client.embeddings(model="example", prompt=row["text"])["embedding"]
    client.upsert(
        collection_name=collection_name,
        points=[{
            "id": index,
            "vector": vector,
        }]
    )


cont = 0

for i in range(len(x)):
    
    cont = search_intent(x['text'][i], cont)
    print(cont)