import time
import os
import requests
from telebot.types import Message
from telebot import TeleBot
from dotenv import load_dotenv
from typing import Final

if not load_dotenv(".env"):
    raise Exception("No envs are set")


BOT_TOKEN = os.environ["BOT_TOKEN"]
LAMBDA_URL = os.environ["LAMBDA_URL"]

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
# TODO: file or kv for tg users

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
    response: str = requests.get(LAMBDA_URL)
    data: dict = response.json()
    bot.send_message(chat_id, f"Response: {str(data)}\n")

def run():
    bot.infinity_polling()


def main():
    run()


if __name__ == '__main__':
    main()
