from event_organization.db.data_access_objects.dao import UserDAO, EventDAO, NotificationDAO
from event_organization.db.models import User, Event, Notification


def test_create_notification(session):
    """ Тестирование создания уведомления """
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

    notification_data = {
        "event_id": event.id,
        "message": "Test Notification",
        "send_time": "2024-12-31 19:00:00"
    }

    notification: Notification = NotificationDAO.add_one(session, notification_data)
    assert notification.event.id == event.id
    assert notification.message == notification_data.get("message")


def test_delete_exist_notification(session):
    """ удаление уведомления """
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

    notification_data = {
        "event_id": event.id,
        "message": "Test Notification",
        "send_time": "2024-12-31 19:00:00"
    }

    notification: Notification | None = NotificationDAO.add_one(session, notification_data)

    NotificationDAO.delete_by_filter(session, **notification_data)
    EventDAO.delete_by_filter(session, **event_data)
    UserDAO.delete_by_filter(session, **user_data)

    notification = NotificationDAO.find_by_filter(session, **notification_data)
    assert notification is None


def test_create_incorrect_event(session):
    """ Тестирование создания уведомления с некорретным event id"""
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
    event_id = event.id
    EventDAO.delete_by_filter(session, **event_data)

    notification_data = {
        "event_id": event_id,
        "message": "Test Notification",
        "send_time": "2024-12-31 19:00:00"
    }

    notification: Notification = NotificationDAO.add_one(session, notification_data)
    assert notification is None


def test_get_event_notifications(session):
    """ Получение списка уведомлений для мероприятия """
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

    notification_data = {
        "event_id": event.id,
        "message": "Test Notification",
        "send_time": "2024-12-31 19:00:00"
    }

    notification: Notification = NotificationDAO.add_one(session, notification_data)

    assert notification in event.notifications
    assert notification.to_dict() in EventDAO.get_event_notifications(session, event.id)