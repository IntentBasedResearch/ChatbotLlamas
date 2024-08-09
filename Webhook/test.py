import pandas as pd

import ollama
from qdrant_client import QdrantClient
from qdrant_client.models import CollectionDescription, Distance, VectorParams

client = QdrantClient(host="127.0.0.1", port=6333)
ollama_client = ollama.Client("http://127.0.0.1:11434")
dataset = pd.read_csv("processed_intent.csv")

# Define collection schema
collection_name = "intent_db"
client.recreate_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(size=4096, distance=Distance.COSINE),
)

# Prepare and index data
for index, row in dataset.iterrows():
    vector = ollama_client.embeddings(model="example", prompt=row["text"])["embedding"]
    client.upsert(
        collection_name=collection_name,
        points=[{
            "id": index,
            "vector": vector,
        }]
    )