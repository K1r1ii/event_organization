from typing import Dict

from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from event_organization.db.exceptions import DataIsNotExists, DataAlreadyExists


class BasDAO:
    model = None

    @classmethod
    def find_by_filter(cls, session: Session, **filters) -> list[Dict] | Dict | None:
        """ Получение данных по фильтрам """
        query = select(cls.model).filter_by(**filters)
        result = session.execute(query)
        res_list = list(map(lambda x: x.to_dict(), result.scalars().all()))
        if len(res_list) == 1:
            return res_list[0]
        return None if res_list == [] else res_list

    @classmethod
    def add_one(cls, session: Session,  values: dict) -> model:
        """ Добавление одного элемента """
        try:
            stmt = insert(cls.model).values(**values).returning(cls.model.id)
            id_col = session.execute(stmt)

            session.commit()

            query = select(cls.model).where(cls.model.id == id_col.scalar())
            result = session.execute(query)
            return result.scalar_one_or_none()
        except IntegrityError:
            return None


    @classmethod
    def update_row(cls, session: Session, new_values: dict, **filters):
        """ Обновление строк  """
        if new_values == {}:
            raise DataIsNotExists("Не указаны поля для обновления")
        stmt = update(cls.model).values(**new_values).filter_by(**filters)
        session.execute(stmt)
        session.commit()


    @classmethod
    def delete_by_filter(cls, session: Session, **filters):
        """ Удаление всех строк соответсвующих фильтрам """
        stmt = delete(cls.model).filter_by(**filters)
        session.execute(stmt)
        session.commit()


    @classmethod
    def clear_table(cls, session: Session):
        """ Очистка всей таблицы """
        session.query(cls.model).delete()
        session.commit()
