import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils.markdown import hbold
from aiogram import F

from app.config import TOKEN
from app.keyboards import Keyboard
from app.parser.wb_parser import get_data
from database.crud import create_product, get_history_user, get_subscription_user
from database.database import Base, engine, SessionDB

# Все обработчики должны быть прикреплены к Маршрутизатору (или Диспетчеру)
dp = Dispatcher()

Base.metadata.create_all(bind=engine)


class ProductInfo(StatesGroup):
	waiting_for_product = State()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
	await message.answer(f"Hello, {hbold(message.from_user.full_name)}!", reply_markup=Keyboard().main_keyboards)


@dp.message(F.text == "Получить информацию по товару")
async def get_data_from_db(message: Message, state: FSMContext):
	await state.set_state(ProductInfo.waiting_for_product)
	await message.answer("Введите артикул товара:", reply_markup=ReplyKeyboardRemove(),)


@dp.message(ProductInfo.waiting_for_product, F.text.isdigit())
async def get_data_from_db(message: Message, state: FSMContext):
	data_product = await get_data(art=message.text, user_id=message.from_user.id)
	if data_product:
		with SessionDB() as db:
			product = create_product(db=db, product=data_product)
			kb = Keyboard(product.article).unsubscribe if product.subscription else Keyboard(product.article).subscribe
			answer = f"{hbold(product.title)}\n\n" \
					 f"артикул: {product.article}\n" \
					 f"цена: {product.price}р.\n" \
					 f"рейтинг: {product.rate}\n" \
					 f"количество на складах: {product.quantity}\n" \
					 f"данные актуальны на {product.date}\n"

		await message.answer(answer, reply_markup=kb)
		await state.clear()
	else:
		await message.answer("Товар не найден")



# Обработчик для кнопки "Остановить"
@dp.message(F.text == "Остановить подписку")
async def stop_processing(message: types.Message):
	with SessionDB() as db:
		history_user = get_subscription_user(db=db, user_id=message.from_user.id)
		if history_user:
			for product in history_user:
				kb = Keyboard().unsubscribe if product.subscription else Keyboard().subscribe
				answer = f"{hbold(product.title)}\n\n" \
						 f"артикул: {product.article}\n" \
						 f"цена: {product.price}р.\n" \
						 f"рейтинг: {product.rate}\n" \
						 f"количество на складах: {product.quantity}\n" \
						 f"данные актуальны на {product.date}\n"

				await message.answer(answer, reply_markup=kb)
		else:
			await message.answer("Подписок нет!")


@dp.message(F.text == "История")
async def get_data_from_db(message: Message):
	with SessionDB() as db:
		history_user = get_history_user(db=db, user_id=message.from_user.id)
		if history_user:
			for product in history_user:
				kb = Keyboard().unsubscribe if product.subscription else Keyboard().subscribe
				answer = f"{hbold(product.title)}\n\n" \
						 f"артикул: {product.article}\n" \
						 f"цена: {product.price}р.\n" \
						 f"рейтинг: {product.rate}\n" \
						 f"количество на складах: {product.quantity}\n" \
						 f"данные актуальны на {product.date}\n"

				await message.answer(answer, reply_markup=kb)
		else:
			await message.answer("История пуста!")


@dp.callback_query(F.data.startswith("sub"))
async def subscribe(callback_query: types.CallbackQuery):
	print(callback_query.data)
	article = callback_query.data.split('_')[1]
	await callback_query.answer(f"Вы подписались на уведомления для товара с артикулом {article}.", cache_time=5)

	while True:
		await asyncio.sleep(10)
		data_product = await get_data(art=article, user_id=callback_query.from_user.id)
		with SessionDB() as db:
			product = create_product(db=db, product=data_product)
			answer = f"{hbold(data_product.get('title'))}\n\n" \
					 f"артикул: {product.article}\n" \
					 f"цена: {product.price}р.\n" \
					 f"рейтинг: {product.rate}\n" \
					 f"количество на складах: {product.quantity}\n" \
					 f"данные актуальны на {product.date}\n"
		await callback_query.message.answer(answer)



async def main() -> None:
	# Инициализируем экземпляр бота с режимом анализа по умолчанию, который будет передаваться всем вызовам API.
	bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
	# И диспетчеризация событий запуска
	await dp.start_polling(bot)


if __name__ == "__main__":
	logging.basicConfig(level=logging.INFO, stream=sys.stdout)
	asyncio.run(main())
