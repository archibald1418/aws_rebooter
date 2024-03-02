import time
import os
import requests
import logging
from requests import Response
from telebot.types import Message
from telebot import TeleBot, logger
from dotenv import load_dotenv
from typing import Final
from fastapi import FastAPI

# if not load_dotenv(".env"):
    # TODO: validation of envs (hint: use a custom config, pydantic may help)
    # raise Exception("No envs are set")

logger.setLevel(logging.DEBUG)

BOT_TOKEN = os.environ["BOT_TOKEN"]
LAMBDA_URL = os.environ["LAMBDA_URL"]

WEBHOOK_HOST = os.environ["WEBHOOK_HOST"]
WEBHOOK_PORT = 8080
WEBHOOK_URL = f'{WEBHOOK_HOST}/api'
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

@app.post(WEBHOOK_URL)
def process_webhook(update: dict):
    print("WEBHOOK CAUGHT!")
    print(update)


def run():
    bot.remove_webhook()
    bot.set_webhook(
        url=WEBHOOK_URL
    )
    print("Bot is running...")
    # bot.infinity_polling()
    print("Bot has finished running")


def main():
    run()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt as e:
        print(e)
