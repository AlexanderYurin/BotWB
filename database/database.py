import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "postgresql://root:root@postgres_db/bot"
SQLALCHEMY_DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}" \
						  f":{os.getenv('DB_PASSWORD')}" \
						  f"@{os.getenv('DB_HOST')}/" \
						  f"{os.getenv('DB_NAME')}"
engine = create_engine(
	SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class SessionDB:
	def __enter__(self):
		self.db = SessionLocal()
		return self.db

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.db.close()
