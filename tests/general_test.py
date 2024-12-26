from event_organization.db.data_access_objects.dao import UserDAO


def test_clear_table(session):
    """ Тестирование очистки таблицы """
    user_data = {
        "name": "Кирилл",
        "email": "test@mail.com",
        "telegram_id": "12345",
        "password": "password"
    }

    user = UserDAO.add_one(session, user_data)

    UserDAO.clear_table(session)

    data = UserDAO.find_by_filter(session)
    assert data is None