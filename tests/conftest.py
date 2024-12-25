import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from event_organization.config import settings
from event_organization.database import Base
from event_organization.db.models import User, Event, EventParticipant, Notification, Bot  # Импорт моделей

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


@pytest.fixture
def test_user(session):
    """ Создание тестового пользователя """
    user = User(name="Test User", email="testuser@example.com", telegram_id="12345", password="password")
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@pytest.fixture
def test_event(session, test_user):
    """ Создание тестового мероприятия """
    event = Event(
        name="Test Event",
        organizer_id=test_user.id,
        description="This is a test event",
        start_time="2024-12-31 18:00:00",
        end_time="2025-01-01 02:00:00",
        location="Test Location",
        created_at="2024-12-25 10:00:00"
    )
    session.add(event)
    session.commit()
    session.refresh(event)
    return event

@pytest.fixture
def test_event_participant(session, test_user, test_event):
    """ Создание тестового участника """
    participant = EventParticipant(event_id=test_event.id, user_id=test_user.id)
    session.add(participant)
    session.commit()
    session.refresh(participant)
    return participant

@pytest.fixture
def test_notification(session, test_event):
    """ Создание тестового уведомления """
    notification = Notification(
        event_id=test_event.id,
        message="Test Notification",
        send_time="2024-12-31 19:00:00"
    )
    session.add(notification)
    session.commit()
    session.refresh(notification)
    return notification
