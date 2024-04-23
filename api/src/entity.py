from pydantic import BaseModel

class UserModel(BaseModel):
    id_hash: int
    admin: bool

class UserEntity:
    def __init__(self, id_hash: int, admin: bool = False):
        self.id_hash = id_hash 
        self.admin = admin
    
    def as_tuple(self) -> tuple[int, bool]:
        return (self.id_hash, self.admin)
