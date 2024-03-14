import asyncio

from aiogram import Router
from aiogram.types import Message
from aiogram import F
from aiogram.utils.markdown import hbold

from app.keyboards import Keyboard
from app.utils import get_answer
from database.crud import get_history_user

route = Router()


@route.message(F.text == "История")
async def get_data_from_db(message: Message):
	history_user = get_history_user(user_id=message.from_user.id)
	if history_user:
		await message.answer(hbold("История последних 5 запросов:\n\n"))
		for i in range(len(history_user)):
			await message.answer(f"{i+1}. {get_answer(history_user[i])}")
	else:
		await message.answer("История пуста!")
