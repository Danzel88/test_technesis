from dataclasses import dataclass


@dataclass(frozen=True)
class BaseAnswer:
    grete_msg: str = "Привет! Загрузи файл для краулер"
    retry_start: str = "Какое-то сообщения при повторном вводе команды /start"
    request_file: str = "Пришли файл для добавления в краулер"
