from fastapi import FastAPI, Request, Response as FastApiResponse, status
from fastapi.responses import JSONResponse

import logging
from typing import AsyncGenerator, Optional, Any

from telebot import TeleBot, logger as tglogger, apihelper
from telebot.types import Message, Update, User
from telebot.apihelper import ApiTelegramException

from contextlib import asynccontextmanager

from .modules.dto import UserDto
from .modules.exceptions import NotAuthorized, Forbidden


from .bot import run_bot
from .session import Sessionizer
from .authorizer import Authorizer
from .config import DB_PATH, WEBHOOK_PATH

from . import db

import os, sys
from pprint import pprint, pformat

#tglogger.setLevel(logging.INFO)

def _sys_info():
    pprint(sys.path)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, Any]:
    print("Start app lifecycle")

    db.init_db(DB_PATH)
    yield
    print("End app lifecycle")


def run_app() -> FastAPI:

    app = FastAPI(
        docs=None, redoc_url=None,
        lifespan=lifespan
    )
    logger = logging.getLogger('uvicorn.error')
    bot = run_bot()
    sessions = Sessionizer(Authorizer(DB_PATH))
    
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

        msg: Message = upd.message
        assert msg.text, "Message is empty"
        if not msg.text.startswith("/"):
            return None # Not a command, ignore

        cmd: str = msg.text.lstrip('/')
        # if cmd not in Authorizer.cmds:
        #     return None  # Not a command, ignore

        # Authorization  (who are you?)
        guest: UserDto = UserDto.from_message(msg)
        print("Hello, guest!: ")
        #pprint(guest.to_dict())
        #logger.log(msg=pformat(guest.to_dict()), level=logging.INFO) 
        try:
            role = sessions.get_or_create_session(guest)
            logger.log(msg=cmd, level=logging.INFO)
            #print(Sessionizer.SESSIONS)
            logger.log(msg=pformat(Sessionizer.SESSIONS), level=logging.INFO)
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
        print("Updates processed ok")
        return JSONResponse(
            status_code=200,
            content={}
        )
    
    return app
