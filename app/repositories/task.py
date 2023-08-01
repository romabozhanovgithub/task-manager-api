from typing import Optional
from uuid import UUID
from sqlalchemy import ScalarSelect, Select, func, literal_column, select, update
from sqlalchemy.dialects.postgresql import insert

from app.models import Task
from app.repositories import BaseRepository
from app.schemas.task import TaskRelationModel, TaskModel


class TaskRepository(BaseRepository):
    __slots__ = ("session",)
    
    model = Task
    schema = TaskRelationModel
    order_by = "task_number"
    limit = 10

    def add_relations(
        self, stmt: Select, project: bool = False, assignee: bool = False
    ) -> Select:
        if project:
            stmt = self.add_relation(stmt, Task.project)
        if assignee:
            stmt = self.add_relation(stmt, Task.assignee)
        return stmt

    def _get_next_task_number(self, project_id: UUID) -> ScalarSelect:
        next_task_number = (
            select(func.coalesce(func.max(Task.task_number) + 1, 1)).
            where(Task.project_id == project_id).
            as_scalar()
        )
        return next_task_number

    async def create(self, project_id: UUID, task: TaskModel) -> TaskRelationModel:
        next_task_number = self._get_next_task_number(project_id)
        stmt = insert(Task).values(
            **task._to_db(),
            task_number=next_task_number,
            project_id=project_id
        ).returning(Task)
        result = await self.session.execute(stmt)
        created_task: Task = result.first()[0]
        new_task = await self.get_by_id(created_task.id)
        await self.session.commit()
        return new_task

    async def get_by_id(
        self, id: UUID, project: bool = True, assignee: bool = True
    ) -> TaskRelationModel | None:
        stmt = self.get(id)
        stmt = self.add_relations(stmt, project, assignee)
        result = await self.execute(stmt)
        task: Task | None = result.one_or_none()
        return self.dump(task)

    async def get_by_project_id(
        self,
        project_id: UUID,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        project: bool = True,
        assignee: bool = True
    ) -> list[TaskRelationModel]:
        stmt = select(Task).where(Task.project_id == project_id)
        stmt = self.add_relations(stmt, project, assignee)
        stmt = self.apply_filters(stmt, limit=limit, offset=offset)
        result = await self.execute(stmt)
        tasks: list[Task] = result.all()
        return self.dump(tasks)
    
    async def get_by_user_id(
        self,
        user_id: UUID,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        project: bool = True,
        assignee: bool = True
    ) -> list[TaskRelationModel]:
        stmt = select(Task).where(Task.assignee_id == user_id)
        stmt = self.add_relations(stmt, project, assignee)
        stmt = self.apply_filters(stmt, limit=limit, offset=offset)
        result = await self.execute(stmt)
        tasks: list[Task] = result.all()
        return self.dump(tasks)

    async def get_by_task_number(
        self,
        project_id: str,
        task_number: int,
        project: bool = False,
        assignee: bool = False,
    ) -> TaskRelationModel | None:
        stmt = self.get_by_field(Task.project_id, project_id)
        stmt = stmt.where(Task.task_number == task_number)
        stmt = self.add_relations(stmt, project, assignee)
        result = await self.execute(stmt)
        task: Task | None = await result.one_or_none()
        return self.dump(task)

    async def get_all(
        self,
        order_by: str | None = None,
        limit: int | None = None,
        offset: int = None,
        ascending: bool = True,
    ) -> list[TaskRelationModel]:
        result = await self.execute(
            super().get_all(order_by, limit, offset, ascending)
        )
        tasks: list[Task] = await result.all()
        return self.dump(tasks)


    async def update(self, id: UUID, task: TaskRelationModel) -> TaskRelationModel:
        await super().update_by_id(
            id, **task._to_db()
        )
        updated_task = await self.get_by_id(id)
        return updated_task

    async def delete(self, id: int) -> bool:
        task: Task = await super().delete_by_id(id)
        return task is not None
