import asyncio

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram import F

from app.keyboards import Keyboard
from app.parser.wb_parser import get_data
from app.utils import get_answer
from database.crud import create_product

import asyncio

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram import F

from app.keyboards import Keyboard
from app.parser.wb_parser import get_data
from app.utils import get_answer
from database.crud import create_product

route = Router()


class SubscriptionProductInfo(StatesGroup):
	product_subscription = State()


@route.callback_query(F.data.startswith("sub"))
async def subscribe(callback_query: CallbackQuery):
	article = callback_query.data.split('_')[1]
	await callback_query.message.reply(f"Вы подписались на уведомления для товара с артикулом {article}.\n"
									   f"Уведомления будут приходить каждые 5 минут.")

	while True:
		await asyncio.sleep(10)
		data_product = await get_data(art=article, user_id=callback_query.from_user.id)
		product = create_product(product=data_product)

		await callback_query.message.answer(get_answer(product))

# async def subscribe(callback_query: types.CallbackQuery):