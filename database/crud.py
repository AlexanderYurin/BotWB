from typing import Dict, List

from sqlalchemy import desc

from database.database import SessionDB
from database.schemas import ProductCreate
from database.models import Product

COUNT_HISTORY = 5


def get_history_user(user_id: int) -> List[Product]:
	"""Получение истории"""
	with SessionDB() as db:
		products = db.query(Product).filter(Product.user_id == user_id).order_by(desc(Product.date)).limit(
			COUNT_HISTORY).all()
		return products


def get_subscription_user(user_id: int) -> List[Product]:
	"""Получить все продукты по подписке"""
	with SessionDB() as db:
		products = db.query(Product).filter(Product.user_id == user_id,
											Product.subscription is True).order_by(desc(Product.date)).all()
		return products


def create_product(product: Dict) -> Product:
	"""Создание и обновления продукта"""
	with SessionDB() as db:
		new_product = ProductCreate(**product)

		db_product = db.query(Product).filter(
			Product.article == new_product.article,
			Product.user_id == new_product.user_id
		).first()
		if db_product:
			db.query(Product).filter(
				Product.id == db_product.id,
			).update(new_product.dict())

		else:
			db_product = Product(**new_product.dict())
			db.add(db_product)

		db.commit()
		db.refresh(db_product)
		return db_product
