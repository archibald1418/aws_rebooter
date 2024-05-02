import logging
from pprint import pprint
import requests

# from contextlib import asynccontextmanager
import sqlite3
import json

import uvicorn
from fastapi import FastAPI, Request, Response as FastApiResponse, status
from fastapi.responses import JSONResponse
from telebot import TeleBot, logger, apihelper
from telebot.types import Message, Update, User
from telebot.apihelper import ApiTelegramException
from typing import TypeAlias, Optional


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
# from db import init_admin, init_db, create_schema, read_users, create_user
import db
from modules.dto import UserDto
from modules.entity import UserEntity
from modules.exceptions import NotAuthorized, Forbidden, AuthException
from session import Sessionizer
from authorizer import Authorizer




# Bot
bot = TeleBot(**DebugBotConfig)
# Database
# db: sqlite3.Connection = sqlite3.connect(DB_FILENAME)
# db.row_factory = UserEntity 

sessions = Sessionizer(Authorizer(DB_FILENAME))
 
# Logging
logger.setLevel(logging.INFO)


@bot.message_handler(commands=["start"])
def on_start(msg: Message):
    bot.send_message(msg.chat.id, MSGS["start"])


@bot.message_handler(commands=["help"])
def help(msg: Message):
    bot.send_message(msg.chat.id, MSGS["help"])


@bot.message_handler(commands=["reboot"])
def on_reboot(msg: Message) -> None:
    chat_id = msg.chat.id
    bot.send_message(chat_id, MSGS["reboot"])
    response: requests.Response = requests.get(LAMBDA_URL)
    data: dict = response.json()
    bot.send_message(chat_id, f"Response: {str(data)}\n")

# @bot.message_handler(commands=['register'])
# def register_use

@bot.message_handler(commands=["get"])
def show_users(msg: Message) -> None:
    # ???: measure response times
    
    users: list[UserEntity] = db.read_users(DB_FILENAME) # db read

    bot.send_message(msg.from_user.id, json.dumps(users))


def parse_user_id(msg: Message) -> int | None:
    assert msg.entities and msg.text
    cmdlen = msg.entities[0].length
    if cmdlen == len(msg.text):
        bot.send_message(msg.from_user.id, "Add a user_id to command")
        return None
    
    user_id = msg.text[cmdlen:].split(maxsplit=2)[0].strip()
    if not user_id.isnumeric() or user_id.startswith('0'):
        bot.send_message(msg.from_user.id, "user_id should be a number")
        return None
    
    try:
        bot.send_message(user_id, f"Checking you, {user_id}") # HACK: maybe there's a better way to check for user_id validity (haven't found one yet)
    except ApiTelegramException as e:
        bot.send_message(msg.from_user.id, "user_id you provided is invalid")
        return None
    new_user_id = int(user_id)
    return new_user_id

@bot.message_handler(commands=["unregister", "delete"])
def unregister_user(msg: Message) -> None:
    if not (user_id :=  parse_user_id(msg)):
        return None
    
    user = UserDto(user_id)
    
    try:
        if db.delete_user(user, DB_FILENAME) == 0:
            raise sqlite3.DatabaseError("User was not deleted because it was not found")
        bot.send_message(msg.from_user.id, f"User {user_id} successfully removed")
    except sqlite3.DatabaseError as e:
        bot.send_message(msg.from_user.id, f"User {user_id} could not be created because of db error")
        bot.send_message(msg.from_user.id, str(e))
        return None

# TODO: study possibilities of using filters
@bot.message_handler(commands=["register", "add"])
def register_user(msg: Message) -> None:
    if not (new_user_id := parse_user_id(msg)):
        return None
    
    new_user = UserDto(new_user_id)

    try:
        db.create_user(new_user, DB_FILENAME)
        bot.send_message(msg.from_user.id, f"User {new_user_id} successfully created")
    except sqlite3.DatabaseError as e:
        bot.send_message(msg.from_user.id, f"User {new_user_id} could not be created because of db error")
        bot.send_message(msg.from_user.id, str(e))
        return None
    
    # ???: measure response times
    # dto: UserDto = UserDto.from_message(msg)
    # new_user: UserEntity = create_user(dto, DB_FILENAME, is_admin=False) # db write

    # bot.send_message(msg.from_user.id, f"New user created:\n {json.dumps(new_user)}")


def run_bot():
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL, drop_pending_updates=True)
    print("Bot is set up...")
    # bot.infinity_polling()
    # print("Bot has finished running")


def run_wsgi():
    print("Wsgi is running!..")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, workers=1)
    print("Wsgi has finished running!..")


async def lifespan(app: FastAPI):
    print("Start app lifecycle")
    run_bot()
    db.init_db(DB_FILENAME)
    yield
    print("End app lifecycle")
    # db.close()


# APP
app = FastAPI(
    docs=None, redoc_url=None
)

@app.exception_handler(AssertionError)
def flow_error(request: Request, exc: AssertionError) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={"error": exc}
    )

@app.get("/")
def root() -> dict:
    return {"Hello": {"Fast": {"Api": {}}}}



@app.post(WEBHOOK_PATH, status_code=200, response_model=None) # pydantic doesn't like None..
def process_webhook(update: dict, response: FastApiResponse) -> Optional[FastApiResponse]:
    print("WEBHOOK CAUGHT UPDATE!")
    assert update, "Update is empty: (webhook seems to have malfunctioned)"
    assert (upd := Update.de_json(update)), "Update is unparseable"

    # pprint(update)
    # assert isinstance(upd, Update)
    # print("update dict: ")
    # pprint(update)
    # print()
    # print("update obj:", type(upd))
    # pprint(upd)

    """
        - Check session
        - If in session, process bot updates
        - If not int session, go to db
        - If not in db, ignore updates
        - If in db, add to session
    """

    msg: Message = upd.message
    assert msg.text, "Message is empty"
    if not msg.text.startswith("/"):
        return None # Not a command, ignore

    cmd: str = msg.text.lstrip('/')
    # if cmd not in Authorizer.cmds:
    #     return None  # Not a command, ignore

    # Authorization  (who are you?)
    guest: UserDto = UserDto.from_message(msg)
    try:
        role = sessions.get_or_create_session(guest)
        print(Sessionizer.SESSIONS)
    except NotAuthorized as e:
        bot.send_message(msg.from_user.id, "You cannot use this bot, sry.. :(")
        return JSONResponse(
            status_code=200,
            content={"error": e.message}
        )

    # Authentication  (what do you want?)
    if cmd in Authorizer.admin_cmds:
        try:
            if not role['admin']:
                raise Forbidden()
        except Forbidden as e:
            bot.send_message(msg.from_user.id, "You cannot run this, try another command.")
            return JSONResponse(
                status_code=200,
                content={"error": e.message}
            )

    # bot.process_middlewares(upd)
    print("Allowing bot to process updates")
    bot.process_new_updates([upd])
    return JSONResponse(
        status_code=200,
        content={}
    )


def main():
    print("MAIN")
    run_bot()
    # init_db(db, DB_FILENAME) <- an extra process locks an sqlite db
    run_wsgi()


def polling_flow():
    print("Polling version")
    db.init_db(DB_FILENAME)
    bot.infinity_polling()


if __name__ == "__main__":
    try:
        print("MAIN")
        print("path ", WEBHOOK_PATH, "\nurl", WEBHOOK_URL)
        main()
        # polling_flow()
    except KeyboardInterrupt as e:
        print(e)
