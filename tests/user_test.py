from sched import Event

import pymysql.err
from sqlalchemy.exc import IntegrityError

from event_organization.db.data_access_objects.dao import UserDAO, EventDAO, EventParticipantDAO
import pytest

from event_organization.db.exceptions import DataIsNotExists
from event_organization.db.models import User, EventParticipant

def test_get_one_user(session):
    """ Тест для получения одного пользовтаеля по фильтрам """
    user_data = {
        "name": "Кирилл",
        "email": "test@mail.com",
        "telegram_id": "12345",
        "password": "password"
    }

    user = UserDAO.add_one(session, user_data)
    user_get_by_filters = UserDAO.find_by_filter(session, **user_data)
    assert user.to_dict() == user_get_by_filters


def test_update_user(session):
    """ Тест для проверки обновления данных пользователя """
    user_data = {
        "name": "Кирилл",
        "email": "test@mail.com",
        "telegram_id": "12345",
        "password": "password"
    }

    user_new_data = {
        "telegram_id": "54321",
        "password": "passwordstrong"
    }

    end_user_data = {
        "name": "Кирилл",
        "email": "test@mail.com",
        "telegram_id": "54321",
        "password": "passwordstrong"
    }

    user = UserDAO.add_one(session, user_data)

    UserDAO.update_row(session, user_new_data, **user_data)

    new_user = UserDAO.find_by_filter(session, **end_user_data)
    assert new_user is not None


def test_incorrect_update_user(session):
    user_data = {
        "name": "Кирилл",
        "email": "test@mail.com",
        "telegram_id": "12345",
        "password": "password"
    }

    user = UserDAO.add_one(session, user_data)

    with pytest.raises(DataIsNotExists):
        UserDAO.update_row(session, {}, **user_data)




def test_create_user(session):
    """ Тестирование создания пользователя """
    user_data = {
        "name": "Кирилл",
        "email": "test@mail.com",
        "telegram_id": "12345",
        "password": "password"
    }

    user = UserDAO.add_one(session, user_data)

    assert user is not None
    assert user.name == "Кирилл"
    assert user.email == "test@mail.com"
    assert user.telegram_id == "12345"


def test_create_exist_user(session):
    """ создание уже существующего пользователя """
    user_data = {
        "name": "Кирилл",
        "email": "test@mail.com",
        "telegram_id": "12345",
        "password": "password"
    }

    user2_data = {
        "name": "Саша",
        "email": "test@mail.com",
        "telegram_id": "12345",
        "password": "password"
    }

    user = UserDAO.add_one(session, user_data)
    user2 = UserDAO.add_one(session, user2_data)
    assert user2 is None


def test_delete_exist_user(session):
    """ Удаление пользователя """
    user_data = {
        "name": "Кирилл",
        "email": "test@mail.com",
        "telegram_id": "12345",
        "password": "password"
    }

    user = UserDAO.add_one(session, user_data)

    UserDAO.delete_by_filter(session, **user_data)

    user = UserDAO.find_by_filter(session, **user_data)
    assert user is None


def test_check_user(session):
    """ Проврека метода для проверки пользователя по почте """
    user_data = {
        "name": "Кирилл",
        "email": "test@mail.com",
        "telegram_id": "12345",
        "password": "password"
    }

    user = UserDAO.add_one(session, user_data)

    user_by_email = UserDAO.check_user_by_email(session, user_data.get("email"))

    assert user == user_by_email


def test_get_user_events(session):
    """ получение всех меропритяий организатора """
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

    event2_data = {
        "name": "Test2 Event",
        "organizer_id": user.id,
        "description": "This is a test event",
        "start_time": "2024-12-31 18:00:00",
        "end_time": "2025-01-01 02:00:00",
        "location": "Test Location",
    }

    event = EventDAO.add_one(session, event_data)
    event2 = EventDAO.add_one(session, event2_data)

    assert len(user.events) == 2
    assert event in user.events
    assert event2 in user.events
    assert event.to_dict() in UserDAO.get_user_events(session, user.id)


def test_get_user_event_participant(session):
    """ Получение всех мероприятий пользователя """
    user_data = {
        "name": "Кирилл",
        "email": "test@mail.com",
        "telegram_id": "12345",
        "password": "password"
    }

    user2_data = {
        "name": "Кирилл2",
        "email": "test2@mail.com",
        "telegram_id": "123456",
        "password": "password"
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

    event2_data = {
        "name": "Test2 Event",
        "organizer_id": user.id,
        "description": "This is a test event",
        "start_time": "2024-12-31 18:00:00",
        "end_time": "2025-01-01 02:00:00",
        "location": "Test Location",
    }

    event = EventDAO.add_one(session, event_data)
    event2 = EventDAO.add_one(session, event2_data)
    participant_data = {
        "event_id": event.id,
        "user_id": user2.id,
        "joined_at": "2024-12-31 18:00:00"
    }

    participant2_data = {
        "event_id": event2.id,
        "user_id": user2.id,
        "joined_at": "2024-12-31 18:00:00"
    }
    participant = EventParticipantDAO.add_one(session, participant_data)
    participant2 = EventParticipantDAO.add_one(session, participant2_data)

    assert participant in user2.event_participants
    assert participant2 in user2.event_participants
    assert participant.to_dict() in UserDAO.get_user_events_participant(session, user2.id)



