import logging
from pprint import pprint
import requests
from requests import Response

# from contextlib import asynccontextmanager
import sqlite3

import uvicorn
from fastapi import FastAPI, Request
from telebot import TeleBot, logger, apihelper
from telebot.types import Message, Update, User

from config import (
    BOT_TOKEN,
    MSGS,
    LAMBDA_URL,
    WEBHOOK_URL,
    WEBHOOK_PATH,
    DB_FILENAME,
    BotConfig,
    DebugBotConfig,
)
from db import init_db
from dto import UserDto
from entity import UserEntity
from session import Sessionizer
from authorizer import Authorizer, NotAuthorized


# Bot
bot = TeleBot(**DebugBotConfig)
apihelper.ENABLE_MIDDLEWARE = True

# Database
# db: sqlite3.Connection = sqlite3.connect(DB_FILENAME)
# db.row_factory = UserEntity 

sessions = Sessionizer(Authorizer())

# Logging
logger.setLevel(logging.INFO)


@bot.message_handler(commands=["start"])
def on_start(msg: Message):
    bot.send_message(msg.chat.id, MSGS["start"])


@bot.message_handler(commands=["help"])
def help(msg: Message):
    bot.send_message(msg.chat.id, MSGS["help"])


@bot.message_handler(commands=["reboot"])
def on_reboot(msg: Message):
    chat_id = msg.chat.id
    bot.send_message(chat_id, MSGS["reboot"])
    response: Response = requests.get(LAMBDA_URL)
    data: dict = response.json()
    bot.send_message(chat_id, f"Response: {str(data)}\n")


def run_bot():
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    print("Bot is set up...")
    # bot.infinity_polling()
    # print("Bot has finished running")


def run_wsgi():
    print("Wsgi is running!..")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, workers=1)
    print("Wsgi has finished running!..")


# async def lifespan(app: FastAPI):
#     assert app
#     print("Start app lifecycle")
#     run_bot()
#     init_db(db, DB_FILENAME)
#     yield
#     print("End app lifecycle")
#     db.close()


def on_startup():
    print("Start app lifecycle")
    run_bot()
    init_db(DB_FILENAME)

def on_shutdown():
    # db.close()
    bot.remove_webhook()
    print("End app lifecycle")


# APP
app = FastAPI(
    docs=None, redoc_url=None, on_startup=[on_startup], on_shutdown=[on_shutdown]
)


@app.get("/")
def root() -> dict:
    return {"Hello": {"Fast": {"Api": {}}}}


@app.post(WEBHOOK_PATH)
def process_webhook(update: dict):
    print("WEBHOOK CAUGHT UPDATE!")
    if not update:
        raise Exception("Update is empty: (webhook seems to have malfunctioned)")
    if not (upd := Update.de_json(update)):
        raise Exception("Update is unparseable")

    assert isinstance(upd, Update)
    print("update dict: ")
    pprint(update)
    print()
    print("update obj:", type(upd))
    pprint(upd)

    """
        - Check session
        - If in session, process bot updates
        - If not int session, go to db
        - If not in db, ignore updates
        - If in db, add to session
    """

    msg: Message = upd.message
    assert msg.text
    if not msg.text.startswith("/"):
        return None  # Not a command, ignore

    # Authorization flow (who are you?)
    guest: UserDto = UserDto.from_message(msg)
    try:
        role = sessions.get_or_create_session(guest)
    except NotAuthorized:
        bot.send_message(msg.from_user.id, "You cannot use this bot, sry.. :(")
        return None

    # Authentication flow (what do you want?)
    # if

    # bot.process_middlewares(upd)
    print("Allowing bot to prcoess updates")
    bot.process_new_updates([upd])


def main():
    print("MAIN")
    run_bot()
    # init_db(db, DB_FILENAME) <- an extra process locks an sqlite db
    run_wsgi()


def polling_flow():
    print("Polling version")
    init_db(DB_FILENAME)
    bot.infinity_polling()


if __name__ == "__main__":
    try:
        print("MAIN")
        print("path ", WEBHOOK_PATH, "\nurl", WEBHOOK_URL)
        main()
        # polling_flow()
    except KeyboardInterrupt as e:
        print(e)
