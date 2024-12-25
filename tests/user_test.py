import pymysql.err
from sqlalchemy.exc import IntegrityError

from event_organization.db.data_access_objects.dao import UserDAO
import pytest

from event_organization.db.models import User


def test_create_user(session):
    """ Тестирование создания пользователя """
    user_data = {
        "name": "Кирилл",
        "email": "test@mail.com",
        "telegram_id": "12345",
        "password": "password"
    }

    user = UserDAO.add_one(session, user_data)

    # Проверка, что пользователь был добавлен в базу
    assert user.id is not None
    assert user.name == "Кирилл"
    assert user.email == "test@mail.com"
    assert user.telegram_id == "12345"


def test_create_exist_user(session):
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
