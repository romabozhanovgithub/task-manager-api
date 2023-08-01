from uuid import UUID
from fastapi import APIRouter, Depends, Request, status

from app.core.dependencies import PaginationParams, TaskIDPath, ProjectIDPath, UserIDPath
from app.core.security import LoginRequired, ManagerPermission, MemberPermission, GuestPermission
from app.schemas.task import CreateTaskSchema, TaskSchema, UpdateTaskSchema, DeleteTaskResponseSchema
from app.services import TaskService

router = APIRouter(
    prefix="/task",
    tags=["task"],
)


@router.get(
    "/project/{project_id}",
    summary="Get all tasks",
    description="Get all tasks",
    dependencies=[Depends(LoginRequired), Depends(GuestPermission)],
    response_model=list[TaskSchema],
    response_model_by_alias=True,
    status_code=status.HTTP_200_OK,
)
async def get_tasks_by_project(
    project_id: UUID = Depends(ProjectIDPath),
    task_service: TaskService = Depends(),
    query_params: dict = Depends(PaginationParams)
) -> list[TaskSchema]:
    tasks = await task_service.get_tasks_by_project(project_id, **query_params)
    return [
        TaskSchema.model_validate(task)
        for task in tasks
    ]


@router.get(
    "/user/me",
    summary="Get all tasks by current user",
    description="Get all tasks by current user",
    dependencies=[Depends(LoginRequired)],
    response_model=list[TaskSchema],
    response_model_by_alias=True,
    status_code=status.HTTP_200_OK,
)
async def get_all_tasks_by_current_user(
    request: Request,
    task_service: TaskService = Depends(),
    query_params: dict = Depends(PaginationParams)
) -> list[TaskSchema]:
    user_id: UUID = request.user.id
    tasks = await task_service.get_tasks_by_user_id(user_id, **query_params)
    return [TaskSchema.model_validate(task) for task in tasks]


@router.get(
    "/user/{user_id}",
    summary="Get all tasks by user id",
    description="Get all tasks by user id",
    dependencies=[Depends(LoginRequired)],
    response_model=list[TaskSchema],
    response_model_by_alias=True,
    status_code=status.HTTP_200_OK,
)
async def get_all_tasks_by_user_id(
    user_id: UUID = Depends(UserIDPath),
    task_service: TaskService = Depends(),
    query_params: dict = Depends(PaginationParams)
) -> list[TaskSchema]:
    tasks = await task_service.get_tasks_by_user_id(user_id, **query_params)
    return [TaskSchema.model_validate(task) for task in tasks]


@router.get(
    "/{project_id}/{task_id}",
    summary="Get task by id",
    description="Get task by id",
    dependencies=[Depends(LoginRequired), Depends(GuestPermission)],
    response_model=TaskSchema,
    response_model_by_alias=True,
    status_code=status.HTTP_200_OK,
)
async def get_task(
    task_id: UUID = Depends(TaskIDPath),
    task_service: TaskService = Depends(),
) -> TaskSchema:
    task = await task_service.get_task(task_id)
    return TaskSchema.model_validate(task)


@router.post(
    "/{project_id}",
    summary="Create task",
    description="Create task",
    dependencies=[Depends(LoginRequired), Depends(MemberPermission)],
    response_model=TaskSchema,
    response_model_by_alias=True,
    status_code=status.HTTP_201_CREATED,
)
async def create_task(
    task: CreateTaskSchema,
    project_id: UUID = Depends(ProjectIDPath),
    task_service: TaskService = Depends(),
) -> TaskSchema:
    new_task = await task_service.create(project_id, task)
    return TaskSchema.model_validate(new_task)


@router.put(
    "/{project_id}/{task_id}",
    summary="Update task",
    description="Update task",
    dependencies=[Depends(LoginRequired), Depends(MemberPermission)],
    response_model=TaskSchema,
    response_model_by_alias=True,
    status_code=status.HTTP_200_OK,
)
async def update_task(
    task: UpdateTaskSchema,
    task_id: UUID = Depends(TaskIDPath),
    task_service: TaskService = Depends(),
) -> TaskSchema:
    task = await task_service.update_task(task_id, task)
    return TaskSchema.model_validate(task)


@router.patch(
    "/complete/{project_id}/{task_id}",
    summary="Complete task",
    description="Complete task",
    dependencies=[Depends(LoginRequired), Depends(MemberPermission)],
    response_model=TaskSchema,
    response_model_by_alias=True,
    status_code=status.HTTP_200_OK,
)
async def complete_task(
    task_id: UUID = Depends(TaskIDPath),
    task_service: TaskService = Depends(),
) -> TaskSchema:
    task = await task_service.complete_task(task_id)
    return TaskSchema.model_validate(task)


@router.delete(
    "/{project_id}/{task_id}",
    summary="Delete task",
    description="Delete task",
    dependencies=[Depends(LoginRequired), Depends(ManagerPermission)],
    response_model=DeleteTaskResponseSchema,
    response_model_by_alias=True,
    status_code=status.HTTP_200_OK,
)
async def delete_task(
    task_id: UUID = Depends(TaskIDPath),
    task_service: TaskService = Depends(),
) -> TaskSchema:
    await task_service.delete_task(task_id)
    return DeleteTaskResponseSchema()
