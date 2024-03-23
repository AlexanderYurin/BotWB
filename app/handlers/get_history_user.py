import asyncio

from aiogram import Router
from aiogram.types import Message
from aiogram import F
from aiogram.utils.markdown import hbold

from app.keyboards import HISTORY
from app.utils import get_answer
from database.crud import get_history_user, COUNT_HISTORY

route = Router()


@route.message(F.text == HISTORY)
async def get_data_from_db(message: Message):
	history_user = get_history_user(user_id=message.from_user.id)
	if not history_user:
		answer = "История пуста!"
	else:
		answer = hbold(f"История последних {COUNT_HISTORY} запросов:\n\n") + \
				 "\n".join(f"{i + 1}. {get_answer(his)}" for i, his in enumerate(history_user))

	await message.answer(answer)
