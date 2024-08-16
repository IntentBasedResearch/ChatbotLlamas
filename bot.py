#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import ollama
from telegram import ForceReply, Update,  Message
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters,CallbackContext
import speech_recognition as sr
import telebot
import subprocess
import os
import requests
import json
import pandas as pd
from voxpopuli import Voice
from gtts import gTTS

from qdrant_client import QdrantClient
from qdrant_client.models import CollectionDescription, Distance, VectorParams

client = QdrantClient(host="127.0.0.1", port=6333)
ollama_client = ollama.Client("http://127.0.0.1:11434")
dataset = pd.read_csv("processed_intent.csv")




# Define a function to search for the closest intent based on user input
def search_intent(user_input, l):
    user_vector = ollama_client.embeddings(model="example", prompt=user_input)["embedding"]
    results = client.search(collection_name="intent_db", query_vector=user_vector, limit=1)

 
    if results:
        best_match: ScoredPoint = results[0]
        print(results)
        print(best_match.score)
        if best_match.score >= 0.90:
            best_match_id = best_match.id
            matched_intent = dataset.iloc[best_match_id]["text"]
            response = dataset.iloc[best_match_id]["nile"]
      
            return "this intent is correct: " + response + " ?"
        elif best_match.score >= 0.30:
            best_match_id = best_match.id
            matched_intent = dataset.iloc[best_match_id]["text"]
            response = dataset.iloc[best_match_id]["nile"]
            print(matched_intent)
            print(response)
            output= ollama.generate(
  model="example",
  prompt=f"this intent: {matched_intent} construct this response: {response}. What this intent: {user_input} construct response?.Response Only UnitIntent"
)
            return output['response']
        else:
          output= ollama.chat(
  model="example",
  messages = l
)
          return output["message"]["content"]
    else:
        return None, "Sorry, I didn't understand that."

bot = telebot.TeleBot("7001357271:AAEQJAWWsgv8Fiu5CIvVcgfkaVbbC5cDu8o")

usuarios = {}



# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    user = requests.get("https://api.telegram.org/bot7001357271:AAEQJAWWsgv8Fiu5CIvVcgfkaVbbC5cDu8o/getUpdates")
    todos = json.loads(user.content)
    if todos['result']!=[]:
        if todos['result'][0]['message']['chat']['id'] not in usuarios:
           
            usuarios[todos['result'][0]['message']['chat']['id']] =[]
    

    usuarios[todos['result'][0]['message']['chat']['id']].append(
    {
      'role': 'user',
      'content': update.message.text,
    }
  )
    x = search_intent(update.message.text,usuarios[todos['result'][0]['message']['chat']['id']])

    usuarios[todos['result'][0]['message']['chat']['id']].append(
    {
      'role': 'assistant',
      'content': x,
    }
  )
    await update.message.reply_text(x)

async def received_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file_size_in_MB = update.message.voice.file_size/(1024*1024)
    print("ok")
    await transcribe(update, context, update.message.voice.duration, file_size_in_MB)

async def received_audio(update: Update, context: CallbackContext):
    
    user = requests.get("https://api.telegram.org/bot7001357271:AAEQJAWWsgv8Fiu5CIvVcgfkaVbbC5cDu8o/getUpdates")
    todos = json.loads(user.content)
    if todos['result']!=[]:
        if todos['result'][0]['message']['chat']['id'] not in usuarios:
           
            usuarios[todos['result'][0]['message']['chat']['id']] =[]
    

    
    
    new_file =  bot.get_file(update.message.voice.file_id)
    r = sr.Recognizer() 
    downloaded_file = bot.download_file(new_file.file_path)
    dst='new_file.wav' 
    with open('new_file.mp3', 'wb') as new_file:
        new_file.write(downloaded_file)
    subprocess.call(['ffmpeg', '-i', 'new_file.mp3',
                   'new_file.wav'])
    user_audio_file = sr.AudioFile('new_file.wav')
    with user_audio_file as source:
        user_audio = r.record(source)
    text = r.recognize_google(user_audio,language="en")
    print(text)
    usuarios[todos['result'][0]['message']['chat']['id']].append(
    {
      'role': 'user',
      'content': text,
    }
  ) 
    x = search_intent(text,usuarios[todos['result'][0]['message']['chat']['id']])

  
    myobj = gTTS(text=x, lang="en", slow=False)
    
    usuarios[todos['result'][0]['message']['chat']['id']].append(
    {
      'role': 'user',
      'content': x,
    }
  )
    
    # Saving the converted audio in a mp3 file named
    # welcome 
   
    myobj.save("welcome.wav")
    user = requests.get("https://api.telegram.org/bot7001357271:AAEQJAWWsgv8Fiu5CIvVcgfkaVbbC5cDu8o/getUpdates")
    todos = json.loads(user.content)
    print(todos['result'][0]['message']['chat']['id'])
    bot.send_audio(chat_id=todos['result'][0]['message']['chat']['id'],audio=open('welcome.wav', 'rb'))

    os.remove('new_file.wav')

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("7001357271:AAEQJAWWsgv8Fiu5CIvVcgfkaVbbC5cDu8o").build()
    
    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.add_handler(MessageHandler(filters.VOICE & (~filters.COMMAND), received_audio))
    # Run the bot until the user presses Ctrl-C
    application.run_polling(timeout=600,allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()