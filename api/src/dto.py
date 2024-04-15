from telebot.types import Update, Message
from datetime import datetime 
from sqlite3 import Cursor
from typing import Self, cast


class UserDto:
    def __init__(self, name, id, dttm):
        self.name: str = name
        self.id: int = id
        self.dttm: datetime = dttm
        # id=uuid.uuid4().int >> 64

    def to_dict(self) -> dict:
        return dict(id=self.id, name=self.name, dttm=self.dttm)

    @classmethod
    def factory(cls, cursor: Cursor, row: tuple) -> Self:
        fields = [column[0] for column in cursor.description]
        return cls(**{
            key: value for key, value in zip(fields, row)
        })
    
    @classmethod
    def from_tgupdate(cls, tgupdate: Update) -> Self:
        msg: Message = cast(Message, tgupdate.message)
        return cls(
                    name=msg.from_user.first_name,
                    id=msg.from_user.id,
                    dttm=msg.date
        )
        
