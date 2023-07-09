from collections.abc import Generator
from datetime import datetime


from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy import Column, String, TIMESTAMP, ARRAY, Integer, Float, ForeignKey, Boolean, create_engine, \
    CheckConstraint, JSON, BigInteger
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base, sessionmaker, Session

DATABASE_URL = "postgresql+asyncpg://postgres:2321@localhost:5432/postgres"
DATABASE_SYNC_URL = 'postgresql+psycopg2://postgres:2321@localhost:5432/postgres'
Base = declarative_base()


class User(Base):  # user model for db
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    registred = Column(TIMESTAMP, default=datetime.utcnow)
    hashed_password = Column(String(256))
    email = Column(String,nullable=False, unique=True)
    phone = Column(String, default=None, nullable=True, unique=True)
    cards = Column(ARRAY(BigInteger), default=[], nullable=True)
    cart = Column(JSON, default={}, nullable=True)
    discounts = Column(JSON, default={}, nullable=True)
    address = Column(String(256), nullable=True)
    sell = Column(Boolean, default=False)
    verify_char = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)


class Product(Base):  # product model for db
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    tags = Column(ARRAY(String), default=[], nullable=True)
    price = Column(Float, nullable=False)
    seller = Column(Integer, ForeignKey(User.id))
    quanity = Column(Integer, nullable=False, default=1)
    discount = Column(Float, CheckConstraint('1 <= discount <= 0'), default=1, nullable=False)

    def dict(self):
        return {'id': self.id,'name': self.name, 'tags': self.tags,'price': self.price, 'seller': self.seller, 'quanity': self.discount, 'quanity': self.discount}


engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

sync_engine = create_engine(DATABASE_SYNC_URL)
sync_session = sessionmaker(sync_engine)


def get_sync_session() -> Generator[Session, None]:
    with sync_session() as session:
        yield session


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


metadata = Base.metadata