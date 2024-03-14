from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from app.keyboards import Keyboard

route = Router()


@route.message(CommandStart())
async def command_start_handler(message: Message) -> None:
	await message.answer(f"Hello, {hbold(message.from_user.full_name)}!", reply_markup=Keyboard().main_keyboards)
