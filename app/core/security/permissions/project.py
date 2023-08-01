from uuid import UUID
from fastapi import Depends, Request

from app.core.dependencies import ProjectIDPath
from app.core.exceptions import NotEnoughPermissionsException
from app.models.user_project import Role
from app.services import ProjectService


class BasePermission:
    __slots__ = ("permission",)

    def __init__(self, permission: Role) -> None:
        self.permission = permission

    def check_permission(self, throw: bool) -> None:
        if not throw:
            raise NotEnoughPermissionsException
        
    async def get_permission(
        self,
        request: Request,
        project_id: UUID,
        project_service: ProjectService
    ) -> Role:
        user_id: UUID = request.user.id
        try:
            result = await project_service.get_user_permissions(
                user_id=user_id, project_id=project_id
            )
            return result.role
        except Exception as e:
            raise NotEnoughPermissionsException
        
    async def __call__(
        self,
        request: Request,
        project_id: UUID = Depends(ProjectIDPath),
        project_service: ProjectService = Depends()
    ) -> bool:
        user_permission = await self.get_permission(
            request=request, project_id=project_id, project_service=project_service
        )
        self.check_permission(self.permission.value >= user_permission.value)


OwnerPermission = BasePermission(Role.OWNER)
ManagerPermission = BasePermission(Role.MANAGER)
MemberPermission = BasePermission(Role.MEMBER)
GuestPermission = BasePermission(Role.GUEST)
