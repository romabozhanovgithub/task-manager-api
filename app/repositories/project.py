from typing import Optional
from uuid import UUID
from sqlalchemy import delete, select, update
from sqlalchemy.dialects.postgresql import insert
from app.models import Project, User
from app.models import user_project, Role
from app.repositories import BaseRepository
from app.schemas.project import ProjectModel, UserInProjectSchema


class ProjectRepository(BaseRepository):
    __slots__ = ("session",)
    
    model = Project
    schema = ProjectModel
    order_by = "title"
    limit = 10

    async def create(self, user_id: UUID, project: ProjectModel) -> ProjectModel:
        new_project = project.to_db()
        self.session.add(new_project)
        await self.session.flush()

        stmt = (
            insert(user_project).
            values(
                user_id=user_id,
                project_id=new_project.id,
                role=Role.OWNER,
            )
        )
        await self.session.execute(stmt)
        await self.session.commit()
        return self.dump(new_project)

    async def get_by_id(self, id: UUID) -> ProjectModel | None:
        result = await self.execute(self.get(id))
        project: Project | None = result.one_or_none()
        return self.dump(project)

    async def get_by_title(self, title: str) -> ProjectModel | None:
        result = await self.execute(self.get_by_field(Project.title, title))
        project: Project | None = result.one_or_none()
        return self.dump(project)
    
    async def get_by_user_id(
        self,
        user_id: UUID,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> list[ProjectModel]:
        stmt = (
            select(Project).
            join(user_project).
            join(User).
            where(user_project.c.user_id == user_id)
        )
        stmt = self.apply_filters(
            statement=stmt,
            limit=limit,
            offset=offset,
        )
        result = await self.execute(stmt)
        projects: list[Project] = result.all()
        return self.dump(projects)
    
    async def get_by_user_and_id(
        self,
        user_id: UUID,
        project_id: UUID
    ) -> UserInProjectSchema | None:
        stmt = (
            select(User, user_project.c.role).
            select_from(user_project).
            join(User, User.id == user_project.c.user_id).
            where(user_project.c.user_id == user_id).
            where(user_project.c.project_id == project_id)
        )
        result = await self.session.execute(stmt)
        user, role = result.first()
        return UserInProjectSchema(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            role=role
        )

    async def get_all(
        self,
        order_by: str | None = None,
        limit: int | None = None,
        offset: int = None,
        ascending: bool = True,
    ) -> list[ProjectModel]:
        result = await self.execute(
            super().get_all(order_by, limit, offset, ascending)
        )
        projects: list[Project] = result.all()
        return self.dump(projects)
    
    async def get_project_users(
        self,
        project_id: UUID,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> list[User]:
        stmt = (
            select(User.id, User.first_name, User.last_name, user_project.c.role).
            select_from(user_project).
            join(User, User.id == user_project.c.user_id).
            where(user_project.c.project_id == project_id).
            offset(offset).
            limit(limit).
            order_by(user_project.c.role)
        )
        result = await self.session.execute(stmt)
        users = result.all()
        return users
    
    async def add_user(
        self, project_id: UUID, user_id: UUID, role: Optional[Role] = None
    ) -> bool:
        values = {
            "project_id": project_id,
            "user_id": user_id,
        }
        if role:
            values["role"] = role
        stmt = (
            insert(user_project).
            values(**values)
        )
        await self.session.execute(stmt)
        await self.session.commit()
        return True
    
    async def update_user(
        self, project_id: UUID, user_id: UUID, role: Role
    ) -> bool:
        stmt = (
            update(user_project).
            where(user_project.c.user_id == user_id).
            where(user_project.c.project_id == project_id).
            where(user_project.c.role != Role.OWNER).
            values(role=role).
            returning(user_project)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        role = result.first()
        if not role:
            return False
        return True

    async def update(self, project_id: UUID, project: ProjectModel) -> ProjectModel:
        project_data = project._to_db()
        updated_project: Project = await super().update_by_id(
            id=project_id,
            **project_data,
        )
        return self.dump(updated_project)
    
    async def delete_user(self, project_id: UUID, user_id: UUID) -> bool:
        stmt = (
            delete(user_project).
            where(user_project.c.user_id == user_id).
            where(user_project.c.project_id == project_id).
            where(user_project.c.role != Role.OWNER).
            returning(user_project.c.user_id)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        deleted_user = result.first()
        if not deleted_user:
            return False
        return True

    async def delete(self, id: UUID) -> ProjectModel | None:
        project: Project = await super().delete_by_id(id)
        return self.dump(project)
