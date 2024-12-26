import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from event_organization.config import settings
from event_organization.database import Base


# Создание подключения к базе данных и сессии
@pytest.fixture(scope="function")
def engine():
    """ Подключение к тестовой базе данных """
    engine = create_engine(settings.get_test_db_url, echo=True)
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def session(engine):
    """ Создание сессии """
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = Session()
    yield session
    session.rollback()
