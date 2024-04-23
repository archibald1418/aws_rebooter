from typing import Protocol, Any
from dto import UserDto
from entity import UserEntity
import sqlite3
from db import read_user, create_user
from config import DB_FILENAME

class NotAuthorized(Exception):
    def __init__(self):
        self.message = 'You are not regisered to use this bot'
        super().__init__(self.message)

class Forbidden(Exception):
    def __init__(self):
        self.message = "You are not allowed to invoke this command"
        super().__init__(self.message)


class Authorizer:
    
    __admin_cmds = {'register', 'get'}

    def encode(self, key: Any) -> int:
        return hash(key)

    def find_user(self, dto: UserDto) -> UserEntity | None:
        encoded_id = self.encode(dto.id)
        with sqlite3.connect(DB_FILENAME) as conn:
            conn.row_factory = UserEntity
            return read_user(conn.cursor(), encoded_id)
        
    def check_admin(self, dto: UserDto) -> bool:
        target_user: UserEntity | None = self.find_user(dto)
        assert target_user
        return bool(target_user.admin)

    def register_user(self, dto: UserDto) -> UserEntity:
        with sqlite3.connect(DB_FILENAME) as conn:
            conn.row_factory = UserEntity
            new_user: UserEntity = create_user(conn.cursor(), self.encode(dto.id))
        return new_user