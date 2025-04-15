import os

import pandas as pd
from pandas import DataFrame
from tgbot.middlewares.db import database


class TableHandler:

    def __init__(self, file_path: str | os.PathLike[str]):
        self.file_path = file_path
        self.df = None

    def read_file(self) -> DataFrame:
        """Читаем файл в DataFrame"""
        raw_table = pd.read_excel(self.file_path, index_col=False)
        self.df = raw_table
        return raw_table

    def __write_df_to_db(self) -> None:
        """Пишем данные из DataFrame в БД"""
        df = self.read_file()
        df.to_sql("graphic_cards", database.connection(), if_exists="append", index=False)

    def process_file(self) -> None:
        """Обработка файла - чтение в DataFrame и запись в БД"""
        self.__write_df_to_db()
