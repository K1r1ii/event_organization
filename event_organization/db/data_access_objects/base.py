from sqlalchemy import select, insert
from sqlalchemy.orm import Session


class BasDAO:
    model = None

    @classmethod
    def find_by_filter(cls, session: Session, **filters):
        """ Получение данных по фильтрам """
        query = select(cls.model).filter_by(**filters)
        result = session.execute(query)
        return result.scalars().all()

    @classmethod
    def add_one(cls, values: dict, session: Session) -> model:
        """ Добавление одного элемента """
        stmt = insert(cls.model).values(**values).returning(cls.model.id)
        id_col = session.execute(stmt)

        session.commit()

        query = select(cls.model).where(cls.model.id == id_col.scalar())
        result = session.execute(query)
        return result.scalar_one_or_none()

