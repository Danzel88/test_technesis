import logging
from pathlib import Path

from aiogram import Router, F, Bot
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from tgbot.config import FORMAT
from tgbot.keyboards.reply import main_kb
from tgbot.misc.dialogs import BaseAnswer
from tgbot.misc.states import UserState
from tgbot.services.table_handler import TableHandler

user_router = Router()


logger = logging.getLogger("user_handler")
logger.setLevel(logging.DEBUG)
sh_uh = logging.StreamHandler()
sh_uh.setFormatter(logging.Formatter(FORMAT))
sh_uh.setLevel(logging.DEBUG)
fh = logging.FileHandler(filename='tgbot/log/users.log')
fh.setFormatter(logging.Formatter(FORMAT))
fh.setLevel(logging.DEBUG)
logger.addHandler(sh_uh)
logger.addHandler(fh)


@user_router.message(CommandStart())
async def user_start(message: Message, state: FSMContext):
    """Создаем пользака в БД. На случай доп метрик. Если уже есть в БД, скажем об этом."""
    await state.clear()
    await message.answer(BaseAnswer.grete_msg, reply_markup=main_kb())


@user_router.message(F.text == "загрузить файл")
async def download_init(message: Message, state: FSMContext):
    """Показываем клавиатуру и инициализируем стэйт ожидания файла"""
    await state.clear()
    await message.answer(BaseAnswer.request_file, reply_markup=ReplyKeyboardRemove())
    await state.set_state(UserState.wait_file)


@user_router.message(UserState.wait_file)
async def get_file(message: Message, bot: Bot, state: FSMContext):
    """Получаем файл, пишем в базу и возвращаем значение пользаку"""
    user_file_id = message.document.file_id
    file_directory = Path(__file__).parent.parent.parent / f"data/{user_file_id[:10]}.xlsx"
    await bot.download(user_file_id, file_directory)
    table_handler = TableHandler(file_directory)
    table_handler.process_file()
    await message.answer(table_handler.read_file().to_string(index=False), reply_markup=main_kb())
    await state.clear()
