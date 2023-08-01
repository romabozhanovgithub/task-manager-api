from typing import Optional
from uuid import UUID
from fastapi import Depends
from sqlalchemy.exc import IntegrityError

from app.core.exceptions import ProjectNotFoundException, ProjectAlreadyExistsException, UserAlreadyInProjectException, UserOrProjectNotFoundException
from app.repositories import ProjectRepository
from app.schemas.project import (
    ProjectModel, CreateProjectSchema, UserProjectSchema, UserInProjectSchema, UpdateUserProjectSchema, UpdateProjectSchema,
)


class ProjectService:
    __slots__ = ("project_repository",)

    def __init__(
        self, project_repository: ProjectRepository = Depends(ProjectRepository)
    ) -> None:
        self.project_repository = project_repository

    async def create(self, user_id: UUID, project: CreateProjectSchema) -> ProjectModel:
        try:
            new_project = await self.project_repository.create(
                user_id=user_id,
                project=ProjectModel.model_validate(project)
            )
        except IntegrityError:
            raise ProjectAlreadyExistsException
        return new_project

    async def get_by_id(self, project_id: UUID) -> ProjectModel | None:
        project = await self.project_repository.get_by_id(
            id=project_id
        )
        if project is None:
            raise ProjectNotFoundException
        return project
    
    async def get_user_permissions(
        self,
        user_id: UUID,
        project_id: UUID
    ) -> UserInProjectSchema:
        user = await self.project_repository.get_by_user_and_id(
            user_id=user_id, project_id=project_id
        )
        if not user:
            raise UserOrProjectNotFoundException
        return user

    async def get_user_projects(
        self,
        user_id: UUID,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> list[ProjectModel]:
        projects = await self.project_repository.get_by_user_id(
            user_id=user_id, limit=limit, offset=offset
        )
        return projects
    
    async def get_project_users(
        self,
        project_id: UUID,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> list[UserInProjectSchema]:
        users = await self.project_repository.get_project_users(
            project_id=project_id, limit=limit, offset=offset
        )
        if not users:
            raise ProjectNotFoundException
        return [
            UserInProjectSchema.model_validate(user)
            for user in users
        ]
    
    async def add_user(
        self, project_id: UUID, add_user: UserProjectSchema
    ) -> bool:
        add_user_data = add_user.model_dump()
        try:
            add = await self.project_repository.add_user(
                project_id=project_id, **add_user_data
            )
        except IntegrityError as e:
            if "duplicate key" in str(e.orig):
                raise UserAlreadyInProjectException
            raise ProjectNotFoundException
        return add
    
    async def update_user(
        self, project_id: UUID, update_user: UpdateUserProjectSchema
    ) -> bool:
        update_user_data = update_user.model_dump()
        update = await self.project_repository.update_user(
            project_id=project_id, **update_user_data
        )
        if not update:
            raise UserOrProjectNotFoundException
        return update
    
    async def update(
        self, project_id: UUID, project: UpdateProjectSchema
    ) -> ProjectModel:
        try:
            updated_project = await self.project_repository.update(
                project_id=project_id, project=ProjectModel.model_validate(project)
            )
        except IntegrityError as e:
            raise ProjectNotFoundException
        return updated_project
    
    async def delete_user(self, project_id: UUID, user_id: UUID) -> bool:
        delete = await self.project_repository.delete_user(
            project_id=project_id, user_id=user_id
        )
        if not delete:
            raise UserOrProjectNotFoundException
        return delete
    
    async def delete(self, project_id: UUID) -> None:
        await self.project_repository.delete(id=project_id)
