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
async def subscribe(callback_query: CallbackQuery, state: FSMContext):
	article = callback_query.data.split('_')[1]
	data = await state.get_data()
	if data.get("article"):
		await callback_query.answer(f"У вас активная подписка на артикул: {article}.\n"
									f"Нажми: Остановить подписку\n", cache_time=10)
		return

	await state.set_state(SubscriptionProductInfo.product_subscription)
	await state.update_data(article=article)

	await callback_query.message.reply(f"Вы подписались на уведомления для товара с артикулом {article}.\n"
								f"Уведомления будут приходить каждые 5 минут.\n")
	while True:
		data = await state.get_data()
		if data.get("sub_status") == "unsub":
			await state.clear()
			break

		data_product = await get_data(art=article, user_id=callback_query.from_user.id)
		product = create_product(product=data_product)
		await callback_query.message.answer(get_answer(product))
		await asyncio.sleep(5)


@route.message(SubscriptionProductInfo.product_subscription, F.text == "Остановить подписку")
async def unsubscribe(message: Message, state: FSMContext):
	await state.update_data(sub_status="unsub")
	await message.reply("Вы успешно отписались от уведомлений.")
