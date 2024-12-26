import uuid

from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from event_organization.db.data_access_objects.base import BasDAO
from event_organization.db.exceptions import InvalidData, DataIsNotExists
from event_organization.db.models import User, Event, EventParticipant, Notification, Bot


class UserDAO(BasDAO):
    model = User

    @classmethod
    def check_user_by_email(cls, session: Session, email: str) -> User | None:
        """ Проврека на существование пользователя по его email """
        user: User | None = session.query(User).where(User.email == email).first()
        return user


    @classmethod
    def get_user_events(cls, session: Session, user_id: uuid.UUID) -> list[dict] | None:
        """ Получить все мероприятия организатора """
        user: User | None = session.query(User).filter_by(id=user_id).first()
        if user:
            return list(map(lambda x: x.to_dict(), user.events))
        return None


    @classmethod
    def get_user_events_participant(cls, session: Session, user_id: uuid.UUID):
        """ Получить все мероприятия пользователя, в которых он учатсвует """
        user: User | None = session.query(User).filter_by(id=user_id).first()
        if user:
            return list(map(lambda x: x.to_dict(), user.event_participants))
        return None


class EventDAO(BasDAO):
    model = Event

    @classmethod
    def add_one(cls, session: Session,  values: dict) -> Event | None:
        """ Добавление одного элемента """
        try:
            if values.get("start_time") > values.get("end_time"):
                raise InvalidData("Некорректное время для события")

            stmt = insert(cls.model).values(**values).returning(cls.model.id)
            id_col = session.execute(stmt)

            session.commit()

            query = select(cls.model).where(cls.model.id == id_col.scalar())
            result = session.execute(query)
            return result.scalar_one_or_none()
        except IntegrityError:
            return None
        except KeyError:
            raise DataIsNotExists("Не достаточно данных для создания события.")


    @classmethod
    def get_event_participants(cls, session: Session, event_id: uuid.UUID) -> list[dict] | None:
        """ Получить всех участников мероприятия """
        event: Event | None = session.query(Event).filter_by(id=event_id).first()
        if event:
            return list(map(lambda x: x.to_dict(), event.participants))
        return None


    @classmethod
    def get_event_bots(cls, session: Session, event_id: uuid.UUID) -> list[dict] | None:
        """ Получить всех ботов для мероприятия """
        event: Event | None = session.query(Event).filter_by(id=event_id).first()
        if event:
            return list(map(lambda x: x.to_dict(), event.bots))
        return None


    @classmethod
    def get_event_notifications(cls, session: Session, event_id: uuid.UUID) -> list[dict] | None:
        """ Получить всех ботов для мероприятия """
        event: Event | None = session.query(Event).filter_by(id=event_id).first()
        if event:
            return list(map(lambda x: x.to_dict(), event.notifications))
        return None


class EventParticipantDAO(BasDAO):
    model = EventParticipant


class NotificationDAO(BasDAO):
    model = Notification


class BotDAO(BasDAO):
    model = Bot
