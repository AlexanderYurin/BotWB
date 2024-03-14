from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from app.keyboards import Keyboard

route = Router()

TEXT = """Я - твой персональный бот для шоппинга с Wildberries! 🛍️

С помощью меня ты можешь получить всю необходимую информацию о товарах, которые тебя интересуют, а также подписаться 
на уведомления о новых поступлениях.

Для начала работы просто выбери одну из кнопок, и мы начнем!🤖✨

Получить информацию по товару - отправь мне артикул товара с Wildberries, и я предоставлю тебе всю информацию о нем.
Остановить уведомления - нажми эту кнопку, если хочешь временно отключить уведомления о новых товарах.
Получить информацию из БД - я могу поделиться последними 5 записями из базы данных."""


@route.message(CommandStart())
async def command_start_handler(message: Message) -> None:
	await message.answer(f"Привет, {hbold(message.from_user.full_name)}!\n{TEXT}",
						 reply_markup=Keyboard().main_keyboards)
