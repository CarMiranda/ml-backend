from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ml_backend.settings import settings

engine = create_engine(settings.POSTGRES_URL, future=True)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
# Base = declarative_base()
