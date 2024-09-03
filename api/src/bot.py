import requests
import json
import sqlite3
from time import sleep

from .config import (
    DebugBotConfig, 
    BotCommands,
    MSGS,
    LAMBDA_URL,
    DB_PATH,
    WEBHOOK_URL
)
from telebot import TeleBot
from telebot.types import Message
from .session import Sessionizer

from .modules.dto import UserDto
from .modules.entity import UserEntity

from . import db, utils

def run_bot() -> TeleBot:

    bot = TeleBot(**DebugBotConfig)

    @bot.message_handler(commands=BotCommands.start)
    def on_start(msg: Message):
        bot.send_message(msg.chat.id, MSGS["start"])
        bot.send_message(msg.chat.id, MSGS["help"])


    @bot.message_handler(commands=BotCommands.help)
    def help(msg: Message):
        bot.send_message(msg.chat.id, MSGS["help"])


    @bot.message_handler(commands=BotCommands.reboot)
    def on_reboot(msg: Message) -> None:
        chat_id = msg.chat.id
        bot.send_message(chat_id, MSGS["reboot"])
        response: requests.Response = requests.get(LAMBDA_URL)
        data: dict = response.json()
        bot.send_message(chat_id, f"Response: {str(data)}\n")


    @bot.message_handler(commands=BotCommands.show)
    def show_users(msg: Message) -> None:
        # ???: measure response times
        
        users: list[UserEntity] = db.read_users(DB_PATH) # db read

        bot.send_message(msg.from_user.id, json.dumps(users))


    @bot.message_handler(commands=BotCommands.unregister)
    def unregister_user(msg: Message) -> None:
        if not (user_id := utils.process_user_id(bot, msg)):
            return None
        
        user = UserDto(user_id)
        
        try:
            if db.delete_user(user, DB_PATH) == 0:
                raise sqlite3.DatabaseError("User was not deleted because it was not found")
            Sessionizer.SESSIONS.pop(user_id, None)
            bot.send_message(user_id, f"You've been kicked out of the bot") # HACK: maybe there's a better way to check for user_id validity (haven't found one yet)
            bot.send_message(msg.from_user.id, f"User {user_id} successfully removed")
        except sqlite3.DatabaseError as e:
            bot.send_message(msg.from_user.id, f"User {user_id} could not be created because of db error")
            bot.send_message(msg.from_user.id, str(e))
            return None


    @bot.message_handler(commands=BotCommands.register)
    def register_user(msg: Message) -> None:
        if not (new_user_id := utils.process_user_id(bot, msg)):
            return None
        
        new_user = UserDto(new_user_id)

        try:
            db.create_user(new_user, DB_PATH)
            bot.send_message(msg.from_user.id, f"User {new_user_id} successfully created")
            bot.send_message(new_user_id, f"You're accepted! Use /help to view commands") # HACK: maybe there's a better way to check for user_id validity (haven't found one yet)
        except sqlite3.DatabaseError as e:
            bot.send_message(msg.from_user.id, f"User {new_user_id} could not be created because of db error")
            bot.send_message(msg.from_user.id, str(e))
            return None
        
        # ???: measure response times

    bot.remove_webhook() # ext api call

    # TODO: test this for when WEBHOOK_URL is not a valid secure-https endpoint
    retries = 0
    while True:
        try:
            bot.set_webhook(url=WEBHOOK_URL, drop_pending_updates=True) # ext api call
        except:
            if retries > 30:
                raise;
            print("Failed to set webhook, retrying...")
            sleep(1)
            retries += 1
        else:
            break
    print("Bot is set up...")

    return bot
