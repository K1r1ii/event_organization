import uuid
from typing import Annotated

from sqlalchemy import String, ForeignKey, UUID
from sqlalchemy.orm import Mapped, MappedColumn

from event_organization.database import Base

id = Annotated[uuid.UUID, MappedColumn(UUID(as_uuid=True), primary_key=True, insert_default=uuid.uuid4)]

class User(Base):
    __tablename__ = "user"
    id: Mapped[id]
    name: Mapped[str] = MappedColumn(String(32), nullable=False)
    email: Mapped[str] = MappedColumn(String(150), nullable=False, unique=True)
