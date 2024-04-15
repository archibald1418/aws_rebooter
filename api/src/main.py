import logging
from pprint import pprint
import requests
from requests import Response 
from contextlib import asynccontextmanager
import sqlite3

import uvicorn
from fastapi import FastAPI
from telebot import TeleBot, logger
from telebot.types import Message, Update, User

from config import BOT_TOKEN, MSGS, LAMBDA_URL, WEBHOOK_URL, WEBHOOK_PATH, DB_FILENAME
from db import init_db
from dto import UserDto

# Bot
bot = TeleBot(BOT_TOKEN, threaded=False)

# Database
db: sqlite3.Connection = sqlite3.connect(DB_FILENAME)
db.row_factory = UserDto.factory

# Logging 
logger.setLevel(logging.INFO)

@bot.message_handler(commands=['start'])
def on_start(msg:Message):
    bot.send_message(msg.chat.id, MSGS['start'])

@bot.message_handler(commands=['help'])
def help(msg:Message):
    bot.send_message(msg.chat.id, MSGS['help'])

@bot.message_handler(commands=['reboot'])
def on_reboot(msg: Message):
    chat_id = msg.chat.id
    bot.send_message(chat_id, MSGS['reboot'])
    response: Response = requests.get(LAMBDA_URL)
    data: dict = response.json()
    bot.send_message(chat_id, f"Response: {str(data)}\n")


def run_bot():
    bot.remove_webhook()
    bot.set_webhook(
        url=WEBHOOK_URL
    )
    print("Bot is set up...")
    # bot.infinity_polling()
    # print("Bot has finished running")

def run_wsgi():
    print("Wsgi is running!..")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    print("Wsgi has finished running!..")


# App lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Start app lifecycle")
    run_bot()
    yield
    print("End app lifecycle")


# APP
app = FastAPI(docs=None, redoc_url=None, lifespan=lifespan)

@app.get("/")
def root() -> dict:
    return {
        "Hello": {
            "Fast": {
                "Api": {}
            }
        }
    }

@app.post(WEBHOOK_PATH)
def process_webhook(update: dict):
    print("WEBHOOK CAUGHT UPDATE!")
    if not update:
        raise Exception("Update is empty: (webhook seems to have malfunctioned)")
    if not (upd := Update.de_json(update)):
        raise Exception("Update is unparseable")
    assert isinstance(upd, Update)
    pprint(update)
    pprint(upd)
    print(type(upd))
    bot.process_new_updates([upd])


def main():
    print("MAIN")
    #run_bot()
    run_wsgi()

# @app.on_event("startup")
# def on_startup():
#     print("on_startup..")
#     run_bot()


if __name__ == '__main__':
    try:
        print("HEY")
        main()
    except KeyboardInterrupt as e:
        print(e)
