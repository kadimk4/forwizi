import aioredis

from fastapi import FastAPI

from fastapi_limiter import FastAPILimiter

from core.user_session import fastapi_users
import redis.asyncio as redis

from src.auth.auth import auth_backend

from src.auth.schemas import UserRead, UserCreate
from src.routes.admin import admin
from src.routes.cart import cart
from src.routes.user import user
from src.routes.verification import verf

app = FastAPI()


@app.on_event("startup")
async def startup():
    red = redis.from_url("redis://localhost", encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(red)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


app.include_router(cart)
app.include_router(admin)
app.include_router(verf)
app.include_router(user)

