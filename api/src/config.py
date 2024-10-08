import os
from sqlite3 import Connection
from typing import Final
from dotenv import load_dotenv

BUILD = os.environ.get("BUILD", "prod")

if BUILD.lower().startswith("dev"):
    if not load_dotenv("../.env.dev"):
        raise Exception("No envs are set")

BOT_TOKEN = os.environ["BOT_TOKEN"]
LAMBDA_URL = os.environ["LAMBDA_URL"]

HOST = os.environ.get("HOST", None)
WEBHOOK_HOST = HOST

# Dev build code
if BUILD == "dev":
    if not load_dotenv("../.env.dev"):
        raise Exception("No envs are set")
    TUNNEL_URL = os.environ["TUNNEL_URL"]
    WEBHOOK_HOST = TUNNEL_URL

BOT_TOKEN = os.environ["BOT_TOKEN"]
LAMBDA_URL = os.environ["LAMBDA_URL"]

WEBHOOK_PORT = 8080
WEBHOOK_PATH = f"/bot/{BOT_TOKEN}"
# well, suffix could be anything, doesn't really matter
WEBHOOK_URL = f"{WEBHOOK_HOST or ''}{WEBHOOK_PATH}"

WEBHOOK_LISTEN = "0.0.0.0"


DB_DIR = "/app/db/"
DB_FILENAME = "users.db" if BUILD.startswith("prod") else "dev.db"
DB_PATH = f"{DB_DIR}{DB_FILENAME}"
ADMIN = int(os.environ["ADMIN"])
TEST_USER = int(os.environ["TEST_USER"])

MSGS: Final[dict] = {
    "start": "Hello, this bot reboots your aws instance\n"
    "/reboot command calls a Lambda function that will do the lightsail reboot",
    "reboot": "Rebooting your lightsail, wait for response...\n",
    "help": "/start - say hi\n"
    "/reboot - reboot AWS Lightsail instance\n"
    "/help - show this message",
}


BotConfig: dict = dict(token=BOT_TOKEN, threaded=False)

DebugBotConfig = BotConfig | dict(skip_pending= True, num_threads=1)

class BotCommands:
    register: Final[list] = ['register', 'add']
    unregister: Final[list] = ['unregister', 'delete']
    start: Final[list] = ['start']
    help: Final[list] = ['help']
    reboot: Final[list] = ['reboot'] # caller only requires List :(
    show: Final[list] = ['get', 'show']
