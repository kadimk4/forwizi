from fastapi import FastAPI

from core.user_session import fastapi_users


from src.auth.auth import auth_backend

from src.auth.schemas import UserRead, UserCreate, UserUpdate
from src.routes.admin import admin
from src.routes.cart import cart
from src.routes.user import user

app = FastAPI()


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

app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

app.include_router(cart)
app.include_router(admin)
app.include_router(user)