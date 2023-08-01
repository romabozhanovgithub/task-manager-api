from uuid import UUID
from fastapi import Path


class TaskIDPathParam:
    def __call__(self, task_id: str = Path(..., min_length=10)) -> UUID:
        return UUID(task_id)
    

TaskIDPath = TaskIDPathParam()
