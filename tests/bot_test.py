from event_organization.db.data_access_objects.dao import UserDAO, EventDAO, BotDAO
from event_organization.db.models import User, Event


def test_get_bots_for_event(session):
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

    bot_data = {
        "event_id": event.id,
        "token": "hksjdhskjdhfkdf",
        "bot_url": "link.ru",
        "instructions": "test test test"
    }

    bot = BotDAO.add_one(session, bot_data)

    assert bot.to_dict() in EventDAO.get_event_bots(session, event.id)
    assert bot in event.bots