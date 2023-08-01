from uuid import UUID
from fastapi import Path


class ProjectIDPathParam:
    def __call__(self, project_id: str = Path(..., min_length=10)) -> UUID:
        return UUID(project_id)
    

ProjectIDPath = ProjectIDPathParam()
