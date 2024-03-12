from typing import Optional, Dict

from pydantic import ValidationError
from sqlalchemy.orm import Session
from sqlalchemy import desc

from database.schemas import ProductCreate
from database.models import Product


def get_history_user(db: Session, user_id: int) -> Optional[Product] | None:
	""" Получить все продукты  """

	products = db.query(Product).filter(Product.user_id == user_id).order_by(desc(Product.date)).all()
	if products:
		return products



def create_product(db: Session, product: Dict):
	try:
		new_product = ProductCreate(**product)
		db_product = Product(**new_product.dict())
		db.add(db_product)
		db.commit()
		db.refresh(db_product)
	except ValidationError as ms:
		print(ms)
	else:
		return db_product

