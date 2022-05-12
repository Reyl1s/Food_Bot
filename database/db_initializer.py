import sqlite3

from config import Config
from multiprocessing.connection import Connection
from sqlite3 import Cursor

class Database:
    config = Config()
    conn: Connection = None
    cursor: Cursor = None

    def __init__(self):
        self.conn = sqlite3.connect(self.config.data['DATABASE_CONN'], check_same_thread=False)
        self.cursor = self.conn.cursor()

    def close_conn(self):
        if(self.conn):
            self.conn.close()