import os
import sqlite3
from sqlite3 import IntegrityError

from tgbot.config import load_config

config = load_config(".env")


class Database:
    __CREATE_REVIEW_TABLE = '''CREATE TABLE graphic_cards(
        id INTEGER PRIMARY KEY,
        title VARCHAR(255),
        url VARCHAR(255),
        xpath VARCHAR(255));'''

    def __init__(self, name=None):
        self.name = name
        self._conn = self.connection()

    def _create_db(self):
        """Создаем базу"""
        connection = sqlite3.connect(self.name)
        cursor = connection.cursor()
        self.__create_tables(self.__CREATE_REVIEW_TABLE, cursor)
        cursor.close()

    def __create_tables(self, table_name, cursor):
        cursor.execute(table_name)

    async def __execute_query(self, query, val):
        cursor = self._conn.cursor()
        try:
            cursor.execute(query, val)
        except IntegrityError:
            self._conn.commit()
            cursor.close()
            return False
        self._conn.commit()
        cursor.close()
        return True

    def connection(self):
        """Конектимся к БД. Если БД нет - создаем её"""
        database_path = os.path.join(os.getcwd(), self.name)
        if not os.path.exists(database_path):
            self._create_db()
        return sqlite3.connect(self.name)

    async def create_item(self, data: dict):
        insert_query = '''INSERT INTO graphic_cards (title, url, xpath) values (?,?,?)'''
        return await self.__execute_query(insert_query, (data['title'], data['url'], data['xpath']))


database = Database(config.db.database)
