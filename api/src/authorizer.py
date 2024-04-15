from typing import Protocol, Any
from dto import UserDto
from entity import UserEntity
from sqlite3 import Connection, Cursor
from db import read_user, create_user

class Authorizer(Protocol):
    
    def check_user(self, dto: UserDto) -> bool: ...
    def encode(self, key: Any) -> int: ...

class NormalAuthorizer(Authorizer):
    
    def __init__(self, db: Connection):
        self.db_cursor: Cursor = db.cursor()

    def encode(self, key: Any) -> int:
        return hash(key)

    def find_user(self, dto: UserDto) -> UserEntity | None:
        encoded_id = self.encode(dto.id)
        target_user: UserEntity | None = read_user(self.db_cursor, encoded_id)
        return target_user
        
    def check_user(self, dto: UserDto) -> bool:
        target_user: UserEntity | None = self.find_user(dto)
        if not target_user:
            return False
        return True

    def register_user(self, dto: UserDto) -> UserEntity:
        new_user: UserEntity = create_user(self.db_cursor, self.encode(dto.id))
        return new_user
        
class AdminAuthorizer(NormalAuthorizer):
    
    def check_user(self, dto: UserDto):
        target_user: UserEntity | None = self.find_user(dto)
        if not target_user or not target_user.admin:
            return False
        return True
