from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware

from app.core import settings
from app.core.security import BearerAuthBackend
from app.db.utils import close_connection
from app.routers import router as api_router

app = FastAPI(
    title=settings.APP_TITLE,
    description=settings.APP_DESCRIPTION,
    debug=settings.DEBUG,
)

# MIDDLEWARES
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(
    AuthenticationMiddleware,
    backend=BearerAuthBackend(),
)

# ROUTES
app.include_router(api_router)


# EVENTS
@app.on_event("startup")
async def startup_event():
    pass


@app.on_event("shutdown")
async def shutdown_event():
    await close_connection()
