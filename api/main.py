import time
import os
import requests
import logging
from pprint import pprint
from requests import Response
from telebot.types import Message, Update, User
from telebot import TeleBot, logger
from dotenv import load_dotenv
from typing import Final
from fastapi import FastAPI
import uvicorn


logger.setLevel(logging.INFO)

BOT_TOKEN = os.environ["BOT_TOKEN"]
LAMBDA_URL = os.environ["LAMBDA_URL"]
BUILD = os.environ["BUILD"]

HOST = os.environ.get("HOST", 'localhost') 

WEBHOOK_HOST = HOST

# Dev build code
if BUILD == 'dev':
    TUNNEL_URL = os.environ["TUNNEL_URL"] 
    WEBHOOK_HOST = TUNNEL_URL
    #if not load_dotenv("../.env.dev"):
    #    raise Exception("No envs are set")
        #TODO: validation of envs (hint: use a custom config, pydantic may help)

WEBHOOK_PORT = 8080
WEBHOOK_PATH = f"/bot/{BOT_TOKEN}"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}" # well, suffix could be anything, doesn't really matter

WEBHOOK_LISTEN = "0.0.0.0"

print(f"===== {WEBHOOK_URL} =====")

MSGS: Final[dict] = {
    'start':
        u'Hello, this bot reboots your aws instance\n'
        u'/reboot command calls a Lambda function that will do the lightsail reboot',
    'reboot':
        u'Rebooting your lightsail, wait for response...\n',
    'help':
        u'/start - say hi\n'
        u'/reboot - reboot AWS Lightsail instance\n'
        u'/help - show this message'
}

bot = TeleBot(BOT_TOKEN, threaded=False)
# TODO: file or kv for tracking of users


app = FastAPI(docs=None, redoc_url=None)

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


# APP
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
    pprint(upd)
    print(type(upd))
    bot.process_new_updates([upd])


def main():
    print("MAIN")
    #run_bot()
    run_wsgi()

@app.on_event("startup")
def on_startup():
    print("on_startup..")
    run_bot()

if __name__ == '__main__':
    try:
        print("HEY")
        main()
    except KeyboardInterrupt as e:
        print(e)
