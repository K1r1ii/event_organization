from typing import Dict

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from config import settings

engine = create_engine(url=settings.get_db_url, echo=False, pool_size=5, max_overflow=10)
SessionFactory = sessionmaker(engine)

class Base(DeclarativeBase):
    __abstract__ = True

    def to_dict(self) -> Dict:
        """Преобразование объекта SQLAlchemy в dict"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


def get_session():
    """ генератор сессий """
    with SessionFactory() as session:
        yield session
