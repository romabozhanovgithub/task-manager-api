from fastapi import HTTPException, status


ProjectNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Project not found",
)

ProjectAlreadyExistsException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Project already exists",
)

UserAlreadyInProjectException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="User already in project",
)

UserOrProjectNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="User or project not found",
)

NotEnoughPermissionsException = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Not enough permissions",
)
