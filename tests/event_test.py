from datetime import datetime

from sqlalchemy.exc import IntegrityError

from event_organization.db.data_access_objects.dao import UserDAO, EventDAO, EventParticipantDAO
import pytest

from event_organization.db.exceptions import InvalidData, DataIsNotExists
from event_organization.db.models import User, Event, EventParticipant


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


def test_create_incorrect_event(session):
    """ Тестирование создания мероприятия с некорректными данными """
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
        "end_time": "2024-12-31 17:00:00",
        "location": "Test Location",
    }

    with pytest.raises(InvalidData):
        event: Event = EventDAO.add_one(session, event_data)


def test_get_all_participants(session):
    user_data = {
        "name": "Кирилл",
        "email": "test@mail.com",
        "telegram_id": "12345",
        "password": "password"
    }

    user2_data = {
        "name": "Миша",
        "email": "test2@mail.com",
        "telegram_id": "123456",
        "password": "password2"
    }

    user: User = UserDAO.add_one(session, user_data)
    user2: User = UserDAO.add_one(session, user2_data)

    event_data = {
        "name": "Test Event",
        "organizer_id": user.id,
        "description": "This is a test event",
        "start_time": "2024-12-31 18:00:00",
        "end_time": "2025-01-01 02:00:00",
        "location": "Test Location",
    }

    event: Event = EventDAO.add_one(session, event_data)

    participant_data = {
        "event_id": event.id,
        "user_id": user2.id,
        "joined_at": "2024-12-31 18:00:00"
    }

    participant = EventParticipantDAO.add_one(session, participant_data)
    assert participant in event.participants
    assert participant.to_dict() in EventDAO.get_event_participants(session, event.id)


def test_delete_participant_for_event(session):
    """ Удаление участника мероприятия """
    user_data = {
        "name": "Кирилл",
        "email": "test@mail.com",
        "telegram_id": "12345",
        "password": "password"
    }

    user2_data = {
        "name": "Миша",
        "email": "test2@mail.com",
        "telegram_id": "123456",
        "password": "password2"
    }

    user: User = UserDAO.add_one(session, user_data)
    user2: User = UserDAO.add_one(session, user2_data)

    event_data = {
        "name": "Test Event",
        "organizer_id": user.id,
        "description": "This is a test event",
        "start_time": "2024-12-31 18:00:00",
        "end_time": "2025-01-01 02:00:00",
        "location": "Test Location",
    }

    event: Event = EventDAO.add_one(session, event_data)

    participant_data = {
        "event_id": event.id,
        "user_id": user2.id,
        "joined_at": "2024-12-31 18:00:00"
    }

    participant = EventParticipantDAO.add_one(session, participant_data)
    EventParticipantDAO.delete_by_filter(session, **participant_data)

    assert event.participants == []


def test_delete_event_with_exist_participant(session):
    user_data = {
        "name": "Кирилл",
        "email": "test@mail.com",
        "telegram_id": "12345",
        "password": "password"
    }

    user2_data = {
        "name": "Миша",
        "email": "test2@mail.com",
        "telegram_id": "123456",
        "password": "password2"
    }

    user: User = UserDAO.add_one(session, user_data)
    user2: User = UserDAO.add_one(session, user2_data)

    event_data = {
        "name": "Test Event",
        "organizer_id": user.id,
        "description": "This is a test event",
        "start_time": "2024-12-31 18:00:00",
        "end_time": "2025-01-01 02:00:00",
        "location": "Test Location",
    }

    event: Event = EventDAO.add_one(session, event_data)

    participant_data = {
        "event_id": event.id,
        "user_id": user2.id,
        "joined_at": "2024-12-31 18:00:00"
    }

    participant = EventParticipantDAO.add_one(session, participant_data)

    with pytest.raises(IntegrityError):
        EventDAO.delete_by_filter(session, **event_data)
