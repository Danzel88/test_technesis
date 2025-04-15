### Системные требования

1. Установленный python <= 3.10
2. Debian 11 или выше

### Настройка

1. Склонировать репозиторий: 
```commandline
git clone https://github.com/Danzel88/test_technesis.git
```

2. Создать в корне бота каталог для логов: 
```commandline
mkdir -p ./test_technesis/tgbot/log
```

3. Создать и активировать виртуальное окружение в каталоге проекта, установить зависимости: 
```commandline
python -m venv test_technesis/.venv
source test_technesis/.venv/bin/activate
pip install -r test_technesis/requirements.txt
```

4. В файле `test_technesis/tgbot.service` заменить ${USER} на имя пользователя, в чем домашнем каталоге будет лежать код проекта. 

5. Переименовать `.env.example`, в `.env` добавить токен бота 
```commandline
mv test_technesis/.env.example test_technesis/.env
```

6. Файл `tgbot.service` копировать в системный каталог и запустить службу:
```commandline
sudo cp test_technesis/tgbot.service /etc/systemd/system/
sudo systemctl enable tgbot.service
sudo systemctl start tgbot.service
```
