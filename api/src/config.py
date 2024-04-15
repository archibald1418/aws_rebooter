import os
from sqlite3 import Connection
from typing import Final

BOT_TOKEN = os.environ["BOT_TOKEN"]
LAMBDA_URL = os.environ["LAMBDA_URL"]
BUILD = os.environ.get("BUILD", 'prod')

HOST = os.environ.get("HOST", None)
WEBHOOK_HOST = HOST

# Dev build code
if BUILD.lower().startswith('dev'):
    TUNNEL_URL = os.environ["TUNNEL_URL"]
    WEBHOOK_HOST = TUNNEL_URL
    #if not load_dotenv("../.env.dev"):
    #    raise Exception("No envs are set")

WEBHOOK_PORT = 8080
WEBHOOK_PATH = f"/bot/{BOT_TOKEN}"
WEBHOOK_URL = f"{WEBHOOK_HOST or ''}{WEBHOOK_PATH}" # well, suffix could be anything, doesn't really matter

WEBHOOK_LISTEN = "0.0.0.0"

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

DB_FILENAME = 'users.db' if BUILD.startswith('prod') else 'dev.db' 