# Create a virtual environment 

python -m venv openai-env

## Enter in virtual environment 

source openai-env/bin/activate

## Install requirements

pip install -r requirements.txt

## Install qdrant image

docker pull qdrant/qdrant
docker run -p 6333:6333 -p 6334:6334 \
-v $(pwd)/qdrant_storage:/qdrant/storage:z \
qdrant/qdrant

## Create a collection 

cd Webhook

Create fisrt a model in llamas: 

python3 qwen.py

Create database in qdrant:

python3 test.py


## Run a boot

Run a model:

python3 model.py

python3 bot.py

Telegram Bot:
https://t.me/IBNLumiChatBot


