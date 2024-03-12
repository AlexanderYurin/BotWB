from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup


class Keyboard:
	@property
	def main_keyboards(self) -> ReplyKeyboardMarkup:
		keyboard_list = [
			[KeyboardButton(text="Получить информацию по товару", data="Tetsa")],
			[KeyboardButton(text="Остановить подписку", callback_data="stop")],
			[KeyboardButton(text="История", callback_data="get_from_db")]
		]
		keyboard = ReplyKeyboardMarkup(
			resize_keyboard=True,
			keyboard=keyboard_list,
			input_field_placeholder="Нажми на кнопку"
		)
		return keyboard

	@property
	def subscribe(self):
		keyboard = [[InlineKeyboardButton(text="подписатьcя", callback_data="sub")]]
		return InlineKeyboardMarkup(inline_keyboard=keyboard)

	@property
	def unsubscribe(self):
		keyboard = [[InlineKeyboardButton(text="отписаться", callback_data="unsub")]]
		return InlineKeyboardMarkup(inline_keyboard=keyboard)
