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


class ProductInfo(StatesGroup):
	waiting_for_product = State()


@route.message(F.text == "Получить информацию по товару")
async def get_info_product(message: Message, state: FSMContext):
	await state.set_state(ProductInfo.waiting_for_product)
	await message.answer("Введите артикул товара:")


@route.message(ProductInfo.waiting_for_product, F.text.isdigit())
async def process_product_info(message: Message, state: FSMContext):
	await message.answer("Идет поиск товара по артикулу!")
	data_product = await get_data(art=message.text, user_id=message.from_user.id)
	if data_product:
		product = create_product(product=data_product)
		await message.answer(get_answer(product), reply_markup=Keyboard(product.article).subscribe)
		await state.clear()
	else:
		await message.answer("Товар не найден. Введите другой артикул!")


@route.message(F("Остановить уведомления"))
async def cmd_stop_notifications(message: Message):
	await message.answer("Уведомления остановлены.")
