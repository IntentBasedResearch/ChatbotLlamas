import pandas as pd
from qdrant_client import QdrantClient
from qdrant_client.models import CollectionDescription, Distance, VectorParams, PointStruct
import ollama

# Initialize clients
client = QdrantClient(host="127.0.0.1", port=6333)
ollama_client = ollama.Client("http://127.0.0.1:11434")

# Load the dataset
dataset = pd.read_csv("processed_intent.csv")




# Define a function to search for the closest intent based on user input
def search_intent(user_input, similarity_threshold=0.8):
    user_vector = ollama_client.embeddings(model="example", prompt=user_input)["embedding"]
    results = client.search(collection_name="intent_db", query_vector=user_vector, limit=1)
      
    if results:
        best_match: ScoredPoint = results[0]
        print(best_match.score)
        if best_match.score >= 0.3:
            best_match_id = best_match.id
            matched_intent = dataset.iloc[best_match_id]["text"]
            response = dataset.iloc[best_match_id]["nile"]
      
            return "this intent is correct: " + response + " ?"
        else:
            output = ollama.generate(
  model="example",
  prompt=f"Respond to this prompt: {user_input}"
) 
            return output["response"]
    else:
        return None, "Sorry, I didn't understand that."

# Simple chat function
def chat():
    print("Welcome to the chat! Type 'exit' to end the conversation.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        
        response = search_intent(user_input)
        print(f"Bot: {response}")

# Start the chat
if __name__ == "__main__":
    chat()