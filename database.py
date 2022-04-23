import sqlite3

from config import get_config
from multiprocessing.connection import Connection
from sqlite3 import Cursor

conn: Connection = None
cursor: Cursor = None

def init_database():
    try:
        global conn
        global cursor

        config = get_config()

        conn = sqlite3.connect(config['DATABASE_CONN'], check_same_thread=False)
        cursor = conn.cursor()

    except sqlite3.Error as error:
        print('Error', error)

def close_conn():
    if(conn):
        conn.close()

def create_user(user_id: int, nickname: str):
    if (cursor):
        user_is_deleted = check_user_is_deleted(user_id)

        if user_is_deleted:
            cursor.execute('UPDATE `Users` SET `Is_Deleted` = false WHERE `User_Id` = ?', (user_id,))
            conn.commit()
        else:
            cursor.execute('INSERT OR IGNORE INTO `Users` (`User_Id`, `Nickname`) VALUES (?,?)', (user_id, nickname))
            conn.commit()

def get_users():
    if (cursor):
        users = cursor.execute('SELECT * FROM `Users` WHERE `Is_Deleted` = 0')
        return users.fetchall()

def get_users_id():
    if (cursor):
        users_id = cursor.execute('SELECT `User_Id` FROM `Users` WHERE `Is_Deleted` = 0')
        return users_id.fetchall()

def get_deleted_users_id():
    if (cursor):
        users_id = cursor.execute('SELECT `User_Id` FROM `Users` WHERE `Is_Deleted` = 1')
        return users_id.fetchall()

def check_user(user_id: int):
    users_id_from_database = get_users_id()

    if len(users_id_from_database) and user_id in users_id_from_database[0]:
        return True
    
    return False

def check_user_is_deleted(user_id: int):
    users_id_from_database = get_deleted_users_id()

    if len(users_id_from_database) and user_id in users_id_from_database[0]:
        return True
    
    return False

def delete_user(user_id: int):
    if (cursor):
        cursor.execute('UPDATE `Users` SET `Is_Deleted` = true WHERE `User_Id` = ?', (user_id,))
        conn.commit()
