from typing import Protocol, Any
import sqlite3
from .modules.dto import UserDto
from .modules.entity import UserEntity
from .db import read_user, create_user # TODO: repo class


class Authorizer:
    
    admin_cmds = frozenset({'register', 'get', 'show', 'delete', 'add'})
    regular_cmds = frozenset({'start', 'help', 'reboot'})
    cmds = admin_cmds | regular_cmds

    def __init__(self, db: str):
        self.db = db # TODO: inject repo class

    def encode(self, key: Any) -> int:
        return hash(key)

    def find_user(self, dto: UserDto) -> UserEntity | None:
        encoded_id = self.encode(dto.id)
        with sqlite3.connect(self.db) as conn:
            # conn.row_factory = UserEntity
            values: tuple | None = read_user(conn.cursor(), encoded_id)
            if not values:
                return None
            return UserEntity.from_tuple(values)
        
    def check_admin(self, dto: UserDto) -> bool:
        target_user: UserEntity | None = self.find_user(dto)
        assert target_user
        return bool(target_user.admin)
