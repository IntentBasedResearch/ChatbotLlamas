# Ollama API Interaction Script

![alt text](images/llava.gif)

# Create a virtual environment 

python -m venv openai-env

## Enter in virtual envioronment

source openai-env/bin/activate

## Install requirements

pip install -r requirements.txt

## Install qdrant image

docker pull qdrant/qdrant
docker run -p 6333:6333 -p 6334:6334 \
-v $(pwd)/qdrant_storage:/qdrant/storage:z \
qdrant/qdrant
