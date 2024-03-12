from datetime import datetime

from pydantic import BaseModel


class ProductCreate(BaseModel):
	article: str
	title: str
	price: float
	rate: float
	quantity: int
	user_id: int
	date: datetime
