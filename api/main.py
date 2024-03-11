import time
import os
import requests
import logging
from requests import Response
from telebot.types import Message, Update, User
from telebot import TeleBot, logger
from dotenv import load_dotenv
from typing import Final
from fastapi import FastAPI
import uvicorn

# if not load_dotenv("../.env"):
    # TODO: validation of envs (hint: use a custom config, pydantic may help)
    # raise Exception("No envs are set")

logger.setLevel(logging.INFO)

BOT_TOKEN = os.environ["BOT_TOKEN"]
LAMBDA_URL = os.environ["LAMBDA_URL"]

WEBHOOK_HOST = os.environ["WEBHOOK_HOST"]
NGROK_TUNNEL_URL='https://90b9-89-180-60-117.ngrok-free.app'
# NGROK_TUNNEL_URL="https://tgbot.free.beeceptor.com" # dev webhook test
WEBHOOK_PORT = 8080
WEBHOOK_PATH = f"/bot/{BOT_TOKEN}"
WEBHOOK_URL = f"{NGROK_TUNNEL_URL}{WEBHOOK_PATH}" # well, suffix could be anything, doesn't really matter
# WEBHOOK_URL = f'{WEBHOOK_HOST}/api/webhook'

# WEBHOOK_URL_BASE = f"{WEBHOOK_HOST}:{WEBHOOK_PORT}"
# WEBHOOK_URL_PATH = "/{}/".format(BOT_TOKEN)
# WEBHOOK_URL = WEBHOOK_URL_BASE + WEBHOOK_URL_PATH
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


#TODO: add webhook
app = FastAPI(docs=None, redoc_url=None)

#TODO: use django or flask as wsgi server


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

@app.post(WEBHOOK_PATH)
def process_webhook(update: dict):
    print("WEBHOOK CAUGHT UPDATE!")
    if not update:
        raise Exception("Update is empty: (webhook seems to have malfunctioned)")
    print(repr(update))
    if not (upd := Update.de_json(update)):
        raise Exception("Update is unparseable")
    bot.process_new_updates([upd])

@app.get("/")
def root() -> dict:
    return {
        "Hello": {
            "Fast": {
                "Api": {}
            }
        }
    }


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

def main():
    run_bot()
    run_wsgi()

# @app.on_event("startup")
# def on_startup():
#     main()

if __name__ == '__main__':
    try:
        print("HEY")
        main()
    except KeyboardInterrupt as e:
        print(e)
