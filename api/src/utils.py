from telebot import TeleBot
from telebot.types import Message
from telebot.apihelper import ApiTelegramException


def process_user_id(bot: TeleBot, msg: Message) -> int | None:
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
        bot.send_message(user_id, f"Checking your user_id") # HACK: maybe there's a better way to check for user_id validity (haven't found one yet)
    except ApiTelegramException as e:
        bot.send_message(msg.from_user.id, "user_id you provided is invalid")
        return None

    new_user_id = int(user_id)
    return new_user_id
