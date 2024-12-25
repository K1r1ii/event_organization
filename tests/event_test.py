import pymysql.err
from sqlalchemy.exc import IntegrityError

from event_organization.db.data_access_objects.dao import UserDAO, EventDAO
import pytest

from event_organization.db.models import User, Event


def test_create_event(session):
    """ Тестирование создания мероприятия """
    user_data = {
        "name": "Кирилл",
        "email": "test@mail.com",
        "telegram_id": "12345",
        "password": "password"
    }

    user: User = UserDAO.add_one(session, user_data)

    event_data = {
        "name": "Test Event",
        "organizer_id": user.id,
        "description": "This is a test event",
        "start_time": "2024-12-31 18:00:00",
        "end_time": "2025-01-01 02:00:00",
        "location": "Test Location",
    }

    event: Event = EventDAO.add_one(session, event_data)

    assert event.name == event_data.get("name")
    assert event.organizer_id == user.id


def test_delete_exist_event(session):
    user_data = {
        "name": "Кирилл",
        "email": "test@mail.com",
        "telegram_id": "12345",
        "password": "password"
    }

    user: User = UserDAO.add_one(session, user_data)

    event_data = {
        "name": "Test Event",
        "organizer_id": user.id,
        "description": "This is a test event",
        "start_time": "2024-12-31 18:00:00",
        "end_time": "2025-01-01 02:00:00",
        "location": "Test Location",
    }

    event = EventDAO.add_one(session, event_data)


    EventDAO.delete_by_filter(session, **event_data)
    UserDAO.delete_by_filter(session, **user_data)

    event = EventDAO.find_by_filter(session, **event_data)
    assert event is None
