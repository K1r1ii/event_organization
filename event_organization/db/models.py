import uuid
from datetime import datetime
from enum import unique
from typing import Annotated

from sqlalchemy import String, ForeignKey, UUID, func, Text, nulls_last
from sqlalchemy.dialects.mssql import TIMESTAMP
from sqlalchemy.orm import Mapped, MappedColumn, relationship

from event_organization.database import Base

id = Annotated[uuid.UUID, MappedColumn(UUID(as_uuid=True), primary_key=True, insert_default=uuid.uuid4)]


class User(Base):
    """ Общий класс пользователей """
    __tablename__ = "user"
    id: Mapped[id]
    name: Mapped[str] = MappedColumn(String(32), nullable=False)
    email: Mapped[str] = MappedColumn(String(150), nullable=False, unique=True)
    telegram_id: Mapped[str] = MappedColumn(String(50), nullable=False, unique=True)
    password: Mapped[str] = MappedColumn(String(100), nullable=False)

    events: Mapped[list["Event"]] = relationship("Event", back_populates="organizer")
    event_participants: Mapped[list["EventParticipant"]] = relationship("EventParticipant", back_populates="user")


class Event(Base):
    """ Модель для события """
    __tablename__ = "event"
    id: Mapped[id]
    name: Mapped[str] = MappedColumn(String(150), nullable=False)
    organizer_id: Mapped[int] = MappedColumn(ForeignKey("user.id"), nullable=False)
    description: Mapped[str] = MappedColumn(Text)
    start_time: Mapped[datetime] = MappedColumn(TIMESTAMP, nullable=False)
    end_time: Mapped[datetime] = MappedColumn(TIMESTAMP, nullable=False)
    location: Mapped[str] = MappedColumn(String(200), nullable=False)
    created_at: Mapped[datetime] = MappedColumn(TIMESTAMP, server_default=func.now())

    organizer: Mapped["User"] = relationship("User", back_populates="events")
    participants: Mapped[list["EventParticipant"]] = relationship("EventParticipant", back_populates="event")
    notifications: Mapped[list["Notification"]] = relationship("Notification", back_populates="event")
    bots: Mapped[list["Bot"]] = relationship("Bot", back_populates="event")


class EventParticipant(Base):
    """ Модель для списка участников """
    __tablename__ = "event_participant"
    id: Mapped[id]
    event_id: Mapped[int] = MappedColumn(ForeignKey("event.id"), nullable=False)
    user_id: Mapped[int] = MappedColumn(ForeignKey("user.id"), nullable=False)
    joined_at: Mapped[datetime] = MappedColumn(TIMESTAMP, server_default=func.now())

    event: Mapped["Event"] = relationship("Event", back_populates="participants")
    user: Mapped["User"] = relationship("User", back_populates="event_participants")


class Notification(Base):
    """ Модель для списка уведомлений """
    __tablename__ = "notification"

    id: Mapped[id]
    event_id: Mapped[int] = MappedColumn(ForeignKey("event.id"), nullable=False)
    message: Mapped[str] = MappedColumn(Text, nullable=False)
    send_time: Mapped[datetime] = MappedColumn(TIMESTAMP, server_default=func.now())

    event: Mapped["Event"] = relationship("Event", back_populates="notifications")


class Bot(Base):
    """ Модель для списка ботов """
    __tablename__ = "bot"

    id: Mapped[id]
    event_id: Mapped[int] = MappedColumn(ForeignKey("event.id"), nullable=False)
    token: Mapped[str] = MappedColumn(String(255), nullable=False)
    bot_url: Mapped[str] = MappedColumn(String(255), nullable=False)
    instructions: Mapped[str] = MappedColumn(Text, nullable=False)

    event: Mapped["Event"] = relationship("Event", back_populates="bots")


