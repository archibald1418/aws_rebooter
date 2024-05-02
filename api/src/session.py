from typing import TypeAlias, Literal, NoReturn
from sqlite3 import DatabaseError
from modules.dto import UserDto
from modules.entity import UserEntity
from modules.exceptions import NotAuthorized, Forbidden
from authorizer import Authorizer

Role: TypeAlias = dict[Literal['admin'], bool]
Session: TypeAlias = dict[int, Role]



class Sessionizer:

    SESSIONS: Session = dict()
    # LIMIT: int = 10 # expiration period

    def __init__(self, authorizer: Authorizer) -> None:
        self.authorizer = authorizer

    def get_or_create_session(self, dto: UserDto) -> Role | NoReturn:
        target_hash = self.authorizer.encode(dto.id)
        try:
            return Sessionizer.SESSIONS[target_hash]
        except KeyError:
            try:
                user: UserEntity | None = self.authorizer.find_user(dto)
            except DatabaseError as de:
                print("Database error caught!: ")
                raise Exception from de
            if not user:
                raise NotAuthorized()
            is_admin = self.authorizer.check_admin(dto)
            Sessionizer.SESSIONS[target_hash] = {'admin' : is_admin}
        # finally:
        
        
        return Sessionizer.SESSIONS[target_hash]

    def delete_session(self, dto: UserDto) -> None:
        target_hash = self.authorizer.encode(dto.id)
        Sessionizer.SESSIONS.pop(target_hash, None)
