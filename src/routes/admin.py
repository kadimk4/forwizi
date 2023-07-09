from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy.orm import Session

from core.user_session import current_user
from src.auth.manager import UserManager
from src.auth.models import User, get_async_session


admin = APIRouter(
    prefix='/admin',
    tags=['admin'])

