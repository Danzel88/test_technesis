from dataclasses import dataclass
from environs import Env


@dataclass
class DbConfig:
    host: str
    database: str


@dataclass
class TgBot:
    token: str
    use_redis: bool


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            use_redis=env.bool("USE_REDIS"),
        ),
        db=DbConfig(
            host=env.str('DB_HOST'),
            database=env.str('DB_NAME')
        ),
    )


FORMAT = '%(asctime)s - %(name)s:%(lineno)s - %(levelname)2s - %(message)s'
