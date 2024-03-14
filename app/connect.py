

import aiohttp
import asyncio

from app.config import HEADERS


async def get_response_text(url: str):
	async with aiohttp.ClientSession(headers=HEADERS) as session:
		async with session.get(url, ssl=False) as resp:
			if resp.status == 200:
				resp_text = await resp.json()
				return resp_text