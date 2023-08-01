from fastapi import APIRouter, Depends, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security.permissions import LoginRequired

from app.schemas.auth import (
    AccessTokenSchema,
    SignUpResponseSchema,
    SignUpUser,
)
from app.schemas.user import ResponseUser
from app.services import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/login",
    summary="Login",
    description="Login",
    response_model=AccessTokenSchema,
    response_model_by_alias=True,
    status_code=status.HTTP_200_OK,
)
async def login(
    data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(),
) -> AccessTokenSchema:
    token = await auth_service.authenticate_user(data.username, data.password)
    return token


@router.post(
    "/signup",
    summary="Sign up",
    description="Sign up",
    response_model=SignUpResponseSchema,
    response_model_by_alias=True,
    status_code=status.HTTP_201_CREATED,
)
async def signup(
    data: SignUpUser,
    auth_service: AuthService = Depends(),
) -> SignUpResponseSchema:
    user = await auth_service.sign_up_user(data)
    return SignUpResponseSchema.model_validate(user)


@router.get(
    "/me",
    summary="Get current user",
    description="Get current user",
    dependencies=[Depends(LoginRequired)],
    response_model=ResponseUser,
    response_model_by_alias=True,
    status_code=status.HTTP_200_OK,
)
async def get_current_user(
    request: Request,
    auth_service: AuthService = Depends(),
) -> ResponseUser:
    request_user = request.user
    user = await auth_service.get_current_user(request_user)
    return ResponseUser.model_validate(user)
