import datetime
from typing import Dict

from aiogram.utils.markdown import hbold

from app.connect import get_response_text

URL = "https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm="


async def get_data(art: str, user_id: int | None = None) -> Dict | None:
	response = await get_response_text(URL + art)
	try:
		response = response["data"]["products"][0]
		data = {
			"article": art,
			"title": response["name"],
			"price": response["salePriceU"] / 100,
			"rate": response["supplierRating"],
			"quantity": sum(stock["qty"] for stock in response["sizes"][0]["stocks"]),
			"user_id": user_id,
			"date": str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
		}
	except IndexError:
		return
	else:
		return data



