import sqlite3
from sqlite3 import Cursor
from modules.dto import UserDto
from modules.entity import UserEntity, UserModel
from config import ADMIN


def create_schema(cursor: Cursor): 
    cursor.execute(f'''CREATE TABLE User (
            id_hash      integer primary key,
            admin   integer(1) default 0
        );
    ''')
    print("Created schema")

def drop_schema(cursor: Cursor):
    cursor.execute(f'''DROP TABLE IF EXISTS User''')
    
def create_user(dto: UserDto, db_filename: str, is_admin: bool = False) -> UserEntity:
    new_user = UserEntity(dto.id, is_admin)
    with sqlite3.connect(db_filename) as conn:
        cursor = conn.cursor()
        cursor.execute(
                '''INSERT INTO User (id_hash, admin) VALUES (?, ?)''',
                new_user.as_tuple()
        )
    '''TODO:
            - all reads should use UserEntity as row_factory
                all writes should create and return a UserEntity (data-access layer)

            - UserDtos should be used on the client-side (business layer)
                UserDtos should be mutually-compatible with UserEntity
    '''
    return new_user
    
def delete_user(cursor: Cursor, user_id: int) -> int:
    return cursor.execute(
            '''DELETE FROM User WHERE id_hash = ?''', [user_id]
        ).rowcount
    
def read_user(cursor: Cursor, user_id: int) -> UserEntity | None:
    cursor.execute(f'''SELECT * FROM User WHERE id_hash = ?''', [user_id])
    return cursor.fetchone()

def read_admin(cursor: Cursor, user_id: int) -> UserEntity:
    cursor.execute(f'''SELECT * FROM User WHERE admin = ? AND id_hash = ?''',
        [True, user_id]
    )
    # TODO: row_factory as factory for select statements
    return cursor.fetchone()

def read_users(db_filename: str) -> list[UserEntity]:
    with sqlite3.connect(db_filename) as conn:
        cursor = conn.cursor()
        cursor.execute(f'''SELECT * from User''')
        return cursor.fetchall()
    
def init_admin(cursor: Cursor):
    cursor.execute(f'''
        INSERT INTO User (id_hash, admin)
                   VALUES (?, ?);
        ''', [ADMIN, 1])

def init_db(db_filename: str) -> None:

    with sqlite3.connect(db_filename) as conn:
        
        cursor: Cursor = conn.cursor()

        try:
            print(f"Creating schema database")
            create_schema(cursor)
            conn.commit()
        except sqlite3.OperationalError:
            print(f"Warn: Database {db_filename} already exists, schema present")
            print("Proceeding...")

        try:
            print("Init db")
            init_admin(cursor)
            conn.commit()
        except Exception as e:
            print(e)
            # The only reliable and legible way to check for schema
