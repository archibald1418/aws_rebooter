from pydantic import BaseModel
from typing import Self

class UserModel(BaseModel):
    id_hash: int
    admin: bool

class UserEntity:
    def __init__(self, id_hash: int, admin: bool = False):
        self.id_hash = id_hash 
        self.admin = admin
    
    def as_tuple(self) -> tuple[int, bool]:
        return (self.id_hash, self.admin)
    
    @classmethod
    def from_tuple(cls, args: tuple[int, bool]) -> Self:
        return cls(*args)

    def __repr__(self):
        return f'<User({self.id_hash}, {self.admin})>'
