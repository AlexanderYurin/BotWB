import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from app.config import TOKEN
from app.handlers import start, get_info_product, get_history_user, stop_subscription
from database.database import Base, engine


async def main():
	bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
	dp = Dispatcher()
	dp.include_routers(start.route, get_info_product.route,
					   get_history_user.route, stop_subscription.route)
	Base.metadata.create_all(bind=engine)

	await bot.delete_webhook(drop_pending_updates=True)
	await dp.start_polling(bot)


if __name__ == "__main__":
	logging.basicConfig(
		level=logging.INFO,
		format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
	)
	asyncio.run(main())
