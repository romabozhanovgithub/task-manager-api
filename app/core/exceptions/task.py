from fastapi import HTTPException, status

TaskAlreadyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Task already exists",
)

TaskNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Task not found",
)
