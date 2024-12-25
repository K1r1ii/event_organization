from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from config import settings

engine = create_engine(url=settings.get_db_url, echo=False, pool_size=5, max_overflow=10)
Session = sessionmaker(engine)

class Base(DeclarativeBase):
    __abstract__ = True


async def get_session():
    """ генератор сессий """
    async with Session as session:
        yield session
