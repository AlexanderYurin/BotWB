from typing import Optional, Dict

from pydantic import ValidationError
from sqlalchemy.orm import Session
from sqlalchemy import desc

from database.database import SessionDB
from database.schemas import ProductCreate
from database.models import Product


def get_history_user(user_id: int) -> Optional[Product] | None:
    with SessionDB() as db:
        products = db.query(Product).filter(Product.user_id == user_id).order_by(desc(Product.date)).limit(5).all()
        if products:
            return products


def get_subscription_user(user_id: int) -> Optional[Product] | None:
    """ Получить все продукты по подписке  """
    with SessionDB() as db:
        products = db.query(Product).filter(Product.user_id == user_id,
                                            Product.subscription is True).order_by(desc(Product.date)).all()
        if products:
            return products


def create_product(product: Dict):
    with SessionDB() as db:
        try:
            new_product = ProductCreate(**product)

            db_product = db.query(Product).filter(
                Product.article == new_product.article,
                Product.user_id == new_product.user_id
            ).first()
            if db_product:
                db.query(Product).filter(
                    Product.article == new_product.article,
                    Product.user_id == new_product.user_id
                ).update(new_product.dict())

            else:
                db_product = Product(**new_product.dict())
                db.add(db_product)

        except ValidationError as ms:
            print(ms)
        else:
            db.commit()
            db.refresh(db_product)
            return db_product
