import sqlite3
from sqlite3 import Cursor
from entity import UserEntity, UserModel


def create_schema(cursor: Cursor): 
    cursor.execute(f'''CREATE TABLE User (
            id_hash      integer primary key,
            admin   integer(1) default 0
        );
    ''')
    print("Created schema")

def drop_schema(cursor: Cursor):
    cursor.execute(f'''DROP TABLE IF EXISTS User''')
    
def create_user(cursor: Cursor, id_hash: int, admin: bool = False) -> UserEntity:
    new_user = UserEntity(id_hash, admin)
    cursor.execute(
            '''INSERT INTO User (id_hash, admin) VALUES (?, ?)''',
            (id_hash, admin)
    )
    return new_user
    
def delete_user(cursor: Cursor, user_id: int) -> int:
    return cursor.execute(
            '''DELETE FROM User WHERE id_hash = ?''', [user_id]
        ).rowcount
    
def read_user(cursor: Cursor, user_id: int) -> UserModel:
    cursor.execute(f'''SELECT * FROM User WHERE id_hash = ?''', [user_id])
    return cursor.fetchone()

def read_admin(cursor: Cursor, user_id: int) -> UserModel:
    cursor.execute(f'''SELECT * FROM User WHERE admin = ? AND id_hash = ?''',
        [True, user_id]
    )
    return cursor.fetchone()

def read_users(cursor: Cursor) -> list[UserModel]:
    cursor.execute(f'''SELECT * from User''')
    return cursor.fetchall()
    
def init_admin(cursor: Cursor):
    cursor.execute(f'''
        INSERT INTO User (id_hash, admin)
                   VALUES (?, ?);
        ''', [42069, 1])

def init_db(conn: sqlite3.Connection, db_filename: str) -> None:

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
