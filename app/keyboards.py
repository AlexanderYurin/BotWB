from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

HISTORY = "История"
STOP_SUB = "Остановить подписку"
GET_INFO = "Получить информацию по товару"


class Keyboard:
	def __init__(self, article=None):
		self.article = article

	@property
	def main_keyboards(self) -> ReplyKeyboardMarkup:
		button1 = KeyboardButton(text=GET_INFO)
		button2 = KeyboardButton(text=STOP_SUB)
		button3 = KeyboardButton(text=HISTORY)

		builder = ReplyKeyboardBuilder().add(button1).row(button2, button3)

		keyboard = builder.as_markup(
			resize_keyboard=True,
			input_field_placeholder="Нажми на кнопку"
		)
		return keyboard

	@property
	def subscribe(self):
		keyboard = [[InlineKeyboardButton(text="подписатьcя", callback_data=f"sub_{self.article}")]]
		return InlineKeyboardMarkup(inline_keyboard=keyboard)

	@property
	def unsubscribe(self):
		keyboard = [[InlineKeyboardButton(text="отписаться", callback_data=f"unsub_{self.article}")]]
		return InlineKeyboardMarkup(inline_keyboard=keyboard)
