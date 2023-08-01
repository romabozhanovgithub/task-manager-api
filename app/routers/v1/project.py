from uuid import UUID
from fastapi import APIRouter, Depends, Request, status

from app.core.dependencies import PaginationParams, ProjectIDPath, UserIDPath
from app.core.security import LoginRequired, OwnerPermission, ManagerPermission, GuestPermission
from app.services import ProjectService
from app.schemas.project import (
    ProjectSchema,
    CreateProjectSchema,
    UserProjectSchema,
    UpdateProjectSchema,
    UpdateUserProjectSchema,
    AddUserResponseSchema,
    UpdateUserResponseSchema,
    RemoveUserResponseSchema,
    DeleteProjectResponseSchema,
    UserInProjectSchema,
)

router = APIRouter(
    prefix="/projects",
    tags=["projects"],
)


@router.get(
    "/",
    summary="Get all projects",
    description="Get all projects",
    dependencies=[Depends(LoginRequired)],
    response_model=list[ProjectSchema],
    response_model_by_alias=True,
    status_code=status.HTTP_200_OK,
)
async def get_all_projects(
    request: Request,
    project_service: ProjectService = Depends(),
    query_params: dict = Depends(PaginationParams)
) -> list[ProjectSchema]:
    user_id: UUID = request.user.id
    projects = await project_service.get_user_projects(
        user_id,
        **query_params
    )
    return [
        ProjectSchema.model_validate(project)
        for project in projects
    ]


@router.get(
    "/{project_id}",
    summary="Get project by id",
    description="Get project by id",
    dependencies=[Depends(LoginRequired), Depends(GuestPermission)],
    response_model=ProjectSchema,
    response_model_by_alias=True,
    status_code=status.HTTP_200_OK,
)
async def get_project_by_id(
    project_id: UUID = Depends(ProjectIDPath),
    project_service: ProjectService = Depends(),
) -> ProjectSchema:
    project = await project_service.get_by_id(project_id)
    return ProjectSchema.model_validate(project)


@router.get(
    "/{project_id}/users",
    summary="Get project users",
    description="Get project users",
    dependencies=[Depends(LoginRequired), Depends(GuestPermission)],
    response_model=list[UserInProjectSchema],
    response_model_by_alias=True,
    status_code=status.HTTP_200_OK,
)
async def get_project_users(
    project_id: UUID = Depends(ProjectIDPath),
    project_service: ProjectService = Depends(),
) -> list[UserInProjectSchema]:
    users = await project_service.get_project_users(project_id)
    return users


@router.post(
    "/",
    summary="Create project",
    description="Create project",
    dependencies=[Depends(LoginRequired)],
    response_model=ProjectSchema,
    response_model_by_alias=True,
    status_code=status.HTTP_201_CREATED,
)
async def create_project(
    request: Request,
    project: CreateProjectSchema,
    project_service: ProjectService = Depends()
) -> ProjectSchema:
    user_id = request.user.id
    project = await project_service.create(user_id, project)
    return ProjectSchema.model_validate(project)


@router.put(
    "/{project_id}",
    summary="Update project",
    description="Update project",
    dependencies=[Depends(LoginRequired), Depends(ManagerPermission)],
    response_model=ProjectSchema,
    response_model_by_alias=True,
    status_code=status.HTTP_200_OK,
)
async def update_project(
    project: UpdateProjectSchema,
    project_id: UUID = Depends(ProjectIDPath),
    project_service: ProjectService = Depends(),
) -> ProjectSchema:
    project = await project_service.update(project_id, project)
    return ProjectSchema.model_validate(project)


@router.patch(
    "/{project_id}/add-user",
    summary="Add user to project",
    description="Add user to project",
    dependencies=[Depends(LoginRequired), Depends(ManagerPermission)],
    response_model=AddUserResponseSchema,
    response_model_by_alias=True,
    status_code=status.HTTP_200_OK,
)
async def add_user_to_project(
    add_user: UserProjectSchema,
    project_id: UUID = Depends(ProjectIDPath),
    project_service: ProjectService = Depends(),
) -> AddUserResponseSchema:
    await project_service.add_user(project_id, add_user)
    return AddUserResponseSchema()


@router.patch(
    "/{project_id}/update-user",
    summary="Update user role in project",
    description="Update user role in project",
    dependencies=[Depends(LoginRequired), Depends(ManagerPermission)],
    response_model=UpdateUserResponseSchema,
    response_model_by_alias=True,
    status_code=status.HTTP_200_OK,
)
async def update_user_in_project(
    update_user: UpdateUserProjectSchema,
    project_id: UUID = Depends(ProjectIDPath),
    project_service: ProjectService = Depends(),
) -> UpdateUserResponseSchema:
    await project_service.update_user(project_id, update_user)
    return UpdateUserResponseSchema()



@router.delete(
    "/{project_id}/remove-user/{user_id}",
    summary="Remove user from project",
    description="Remove user from project",
    dependencies=[Depends(LoginRequired), Depends(ManagerPermission)],
    response_model=RemoveUserResponseSchema,
    response_model_by_alias=True,
    status_code=status.HTTP_200_OK,
)
async def remove_user_from_project(
    user_id: UUID = Depends(UserIDPath),
    project_id: UUID = Depends(ProjectIDPath),
    project_service: ProjectService = Depends(),
) -> RemoveUserResponseSchema:
    await project_service.delete_user(project_id, user_id)
    return RemoveUserResponseSchema()


@router.delete(
    "/{project_id}",
    summary="Delete project",
    description="Delete project",
    dependencies=[Depends(LoginRequired), Depends(OwnerPermission)],
    response_model=DeleteProjectResponseSchema,
    response_model_by_alias=True,
    status_code=status.HTTP_200_OK,
)
async def delete_project(
    project_id: UUID = Depends(ProjectIDPath),
    project_service: ProjectService = Depends(),
) -> DeleteProjectResponseSchema:
    await project_service.delete(project_id)
    return DeleteProjectResponseSchema()
