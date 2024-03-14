from sqlalchemy import Column, Integer, String, TIMESTAMP, Float, BigInteger, BOOLEAN

from database.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    article = Column(String)
    title = Column(String)
    price = Column(Float)
    rate = Column(Float)
    quantity = Column(BigInteger)
    user_id = Column(BigInteger)
    date = Column(TIMESTAMP)
    subscription = Column(BOOLEAN, default=False)
