from datetime import datetime
from enum import Enum
from typing import Optional, List
import re
from fastapi_users import schemas
from pydantic import EmailStr, validator, BaseModel
from fastapi import HTTPException
validate_list = [',', '"', "'", ':', ':', '/', '?', '[', ']', '{', '}', '\\', '!', '@', '#', '$', '%', '^', '&', '*',
                 '(',')', '-', '_', '+', '=', "№"]


class UserRead(schemas.BaseUser[int]):
    email: EmailStr
    first_name: str
    last_name: str
    registred: datetime
    cards: list[str] | None
    phone: str | None
    address: str
    discount: list[str]
    # is_active: bool = True
    # is_superuser: bool = False
    is_verified: bool = False


class UserCreate(schemas.BaseUserCreate):
    first_name: str
    last_name: str
    password: str
    email: EmailStr
    # address: str
    # phone: str
    # cards: list[int] | None
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False

    # @validator('phone')
    # def validate_phone(cls, value):
    #     result = bool(re.match(r'^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$', value))
    #     if result:
    #         return value
    #     raise HTTPException(status_code=400, detail='uncorrent phone number')

    @validator('first_name')
    def validate_name(cls, value):
        if value[0].isupper() and len(value) >= 2 and len(value) <= 26:
            for i in value:
                if i in validate_list or i.isdigit():
                    raise HTTPException(status_code=400, detail='incorrent fist name')
            return value
        raise HTTPException(status_code=400, detail='incorrent first name')

    @validator('last_name')
    def validate_last_name(cls, value):
        if value[0].isupper() and len(value) >= 2 and len(value) <= 40:
            for i in value:
                if i in validate_list or i.isdigit():
                    raise HTTPException(status_code=400, detail='incorrent last name')
            return value
        raise HTTPException(status_code=400, detail='incorrent last name')

    # @validator('cards', check_fields=False)
    # def validate_card(cls, value):
    #     for i in value:
    #         if len(str(i)) != 16:
    #             raise HTTPException(status_code=400, detail='incorrent card')
    #         return value


class Discount(BaseModel):
    named: str
    amount: float = 1


class Tags(str, Enum):
    fruits: str = 'Фрукты'
    vegetables: str = 'Овощи'
    berries: str = 'Ягоды'
    exotic: str = 'Экзотические'
    sales: str = 'Скидки'


class Product(BaseModel):
    name: str
    quanity: int = 1
    price: float = 1
    discount: float | None = 1



class UserUpdate(schemas.BaseUserUpdate):
    pass