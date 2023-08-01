from fastapi import APIRouter

from app.routers.v1.auth import router as auth_router
from app.routers.v1.project import router as project_router
from app.routers.v1.task import router as task_router

router = APIRouter(
    prefix="/v1",
    tags=["v1"],
)

router.include_router(auth_router)
router.include_router(project_router)
router.include_router(task_router)

__all__ = [
    "router",
]
