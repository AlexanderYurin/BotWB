from dotenv import load_dotenv, find_dotenv
import os


if not find_dotenv():
	exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
	load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) '
						 'AppleWebKit/537.36 (KHTML, like Gecko) '
						 'Chrome/105.0.0.0 Safari/537.36 '}