from typing import Optional, TypeVar
from sqlalchemy import (
    Column,
    ScalarResult,
    Select,
    select,
    update,
    delete,
    asc,
    desc,
)
from sqlalchemy.orm import joinedload, lazyload, selectinload, subqueryload
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.db.utils import get_session
from app.models.base import Base
from app.schemas.base import ModelSchema

Model = TypeVar("Model", bound="Base")
Schema = TypeVar("Schema", bound="ModelSchema")


class BaseRepository:
    model: Model
    schema: Schema
    session: AsyncSession
    order_by: str
    limit: int | None

    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session: AsyncSession = session

    def _paginate(
        self, statement: Select, limit: int | None = None, offset: int = 0
    ) -> Select:
        """
        Paginate a select statement.
        Returns a select statement.
        """

        if limit is not None:
            statement = statement.limit(limit)
        else:
            statement = statement.limit(self.limit)
        statement = statement.offset(offset)
        return statement

    def _order_by(
        self,
        statement: Select,
        order_by: str | None = None,
        ascending: bool = True,
    ) -> Select:
        """
        Order a select statement.
        Returns a select statement.
        """

        if ascending:
            sort = asc
        else:
            sort = desc
        if order_by is not None:
            statement = statement.order_by(sort(order_by))
        else:
            statement = statement.order_by(sort(self.order_by))
        return statement

    def apply_filters(
        self,
        statement: Select,
        order_by: str | None = None,
        limit: int | None = None,
        offset: int = 0,
        ascending: bool = True,
    ) -> Select:
        """
        Apply filters to a select statement.
        Returns a select statement.
        """

        statement = self._order_by(statement, order_by, ascending)
        statement = self._paginate(statement, limit, offset)
        return statement

    def add_relation(
        self,
        stmt: Select,
        field: Column,
        subquery: bool = False,
        select: bool = False,
        lazy: bool = False,
    ) -> Select:
        """
        Returns a relationship statement.
        """

        if lazy:
            stmt = stmt.options(lazyload(field))
        elif subquery:
            stmt = stmt.options(subqueryload(field))
        elif select:
            stmt = stmt.options(selectinload(field))
        else:
            stmt = stmt.options(joinedload(field))
        return stmt

    async def execute(self, stmt: Select) -> ScalarResult:
        """
        Execute a select statement.
        Returns a model or a list of models.
        """

        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalars()

    async def create(self, inst: Model) -> Model:
        """
        Create a new record in the database.
        Rolls back the transaction if an exception occurs.
        Returns the created model.
        """

        self.session.add(inst)
        await self.session.commit()
        return inst

    def get(self, id: int) -> Select:
        """
        Get a record from the database.
        Returns a select statement.
        """

        stmt = select(self.model).where(self.model.id == id)
        return stmt

    def get_by_field(self, field: Column, value: str) -> Select:
        """
        Get a record from the database by field.
        Returns a select statement.
        """

        stmt = select(self.model).where(field == value)
        return stmt

    def get_all(
        self,
        order_by: str | None = None,
        limit: int | None = None,
        offset: int = 0,
        ascending: bool = True,
    ) -> Select:
        """
        Get all records from the database.
        Returns a select statement.
        """

        stmt = select(self.model)
        stmt = self.apply_filters(stmt, order_by, limit, offset, ascending)
        return stmt

    def filter(
        self,
        order_by: str | None = None,
        limit: int | None = None,
        offset: int = 0,
        ascending: bool = True,
        **kwargs: dict
    ) -> list[Model]:
        """
        Filter records from the database.
        Returns a select statement.
        """

        stmt = select(self.model).filter_by(**kwargs)
        stmt = self.apply_filters(stmt, order_by, limit, offset, ascending)
        return stmt

    async def update(self, inst: Schema) -> Model:
        """
        Update a record in the database.
        Rolls back the transaction if an exception occurs.
        Returns the updated model.
        """

        updated_inst = await self.update_by_id(inst.id, **inst._to_db())
        return updated_inst

    async def update_by_id(self, id: int, **kwargs: dict) -> Model | None:
        """
        Update a record in the database by id.
        Rolls back the transaction if an exception occurs.
        Returns the updated model.
        """

        stmt = (
            update(self.model)
            .where(self.model.id == id)
            .values(**kwargs)
            .returning(self.model)
        )
        result = await self.execute(stmt)
        return result.one_or_none()

    async def delete(self, inst: Model) -> Model:
        """
        Delete a record from the database.
        Rolls back the transaction if an exception occurs.
        Returns the deleted model.
        """

        self.session.delete(inst)
        await self.session.commit()
        return inst

    async def delete_by_id(self, id: int) -> Model | None:
        """
        Delete a record from the database by id.
        Rolls back the transaction if an exception occurs.
        Returns the deleted model.
        """

        stmt = (
            delete(self.model).where(self.model.id == id).returning(self.model)
        )
        result = await self.execute(stmt)
        return result.one_or_none()

    def dump(
        self, inst: Optional[Model | list[Model]] = None
    ) -> Schema | list[Schema] | None:
        """
        Dump a model to a Schema.
        Returns a Schema.
        """

        if inst is None:
            return inst

        if isinstance(inst, self.model):
            return self.schema.model_validate(inst)
        elif isinstance(inst, list):
            return [
                self.schema.model_validate(model_inst) for model_inst in inst
            ]
