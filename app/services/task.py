from typing import Optional
from uuid import UUID
from fastapi import Depends
from sqlalchemy.exc import IntegrityError

from app.core.exceptions import TaskAlreadyExistsException, TaskNotFoundException, ProjectNotFoundException, UserNotFoundException
from app.repositories import TaskRepository
from app.schemas.task import TaskModel, CreateTaskSchema, UpdateTaskSchema


class TaskService:
    __slots__ = ("task_repository",)

    def __init__(
        self, task_repository: TaskRepository = Depends(TaskRepository)
    ) -> None:
        self.task_repository = task_repository

    async def create(self, project_id: UUID, task: CreateTaskSchema) -> TaskModel:
        try:
            new_task = await self.task_repository.create(
                project_id=project_id,
                task=TaskModel.model_validate(task)
            )
        except IntegrityError as e:
            if "insert" in str(e.orig):
                raise ProjectNotFoundException
            raise TaskAlreadyExistsException
        return new_task
    
    async def get_task(self, task_id: UUID) -> TaskModel | None:
        task = await self.task_repository.get_by_id(
            id=task_id
        )
        if task is None:
            raise TaskNotFoundException
        return task
    
    async def get_tasks_by_project(
        self, project_id: UUID, limit: Optional[int] = None, offset: Optional[int] = None
    ) -> list[TaskModel]:
        tasks = await self.task_repository.get_by_project_id(
            project_id=project_id, limit=limit, offset=offset
        )
        return tasks
    
    async def get_tasks_by_user_id(
        self, user_id: UUID, limit: Optional[int] = None, offset: Optional[int] = None
    ) -> list[TaskModel]:
        tasks = await self.task_repository.get_by_user_id(
            user_id=user_id, limit=limit, offset=offset
        )
        return tasks
    
    async def update_task(self, task_id: UUID, task: UpdateTaskSchema) -> TaskModel:
        update_task = TaskModel.model_validate(task)
        try:
            updated_task = await self.task_repository.update(
                id=task_id, task=update_task
            )
        except IntegrityError:
            raise UserNotFoundException
        if updated_task is None:
            raise TaskNotFoundException
        return updated_task
    
    async def complete_task(self, task_id: UUID) -> TaskModel:
        completed_task = await self.task_repository.update(
            id=task_id, task=TaskModel(completed=True)
        )
        if completed_task is None:
            raise TaskNotFoundException
        return completed_task
    
    async def delete_task(self, task_id: UUID) -> None:
        deleted_task = await self.task_repository.delete(
            id=task_id
        )
        if not deleted_task:
            raise TaskNotFoundException
