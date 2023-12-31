import json
from typing import List

from fastapi import APIRouter, Depends, Form
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy.orm import Session

from core.user_session import current_user
from src.auth.models import User, get_async_session, Product as Product, get_sync_session
from src.auth.schemas import Product as ProductP, Tags

cart = APIRouter(
    prefix='/cart',
    tags=['cart'])


@cart.get('/')
async def get_cart(user: User = Depends(current_user), session: Session = Depends(get_sync_session)):
    try:
        user = session.query(User).where(User.id == user.id).first()
        return user.cart
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'something wrong, {e}')


@cart.post('/add') # post new product
async def past_product(product: ProductP, tags: Tags,user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)):
    try:
        new_product = Product(name=product.name, price=product.price, discount=product.discount, quanity=product.quanity, seller=user.id, tags=tags)
        session.add(new_product)
        await session.commit()
        return {
            'status': 'added'
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'something wrong, {e}')


@cart.get('/information') # Information about product
def check_product(product: str, session: Session = Depends(get_sync_session)):
    try:
        prod = session.query(Product).where(Product.name == product).all()
        result = [ProductP(**i.dict()) for i in prod]
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'not found, {e}')


@cart.patch('/add_to_cart') # add product to user cart
async def add_product(product_id: int | None = None, count: int = 1, session: AsyncSession = Depends(get_async_session),
                      user: User = Depends(current_user)):
    try:
        product = await session.get(Product, product_id)
        if not product:
            raise HTTPException(status_code=404, detail='Product not found')

        cart_data = user.cart or {}
        cart_data[product.name] = cart_data.get(product.name, 0) + count
        user.cart = cart_data
        await session.commit()
        return {
            'status': 'successful'
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'not found {product.name} {e}')


@cart.patch('/remove_product_from_cart')
async def remove_product(product_id: int | None = None, count: int = 1, session: Session = Depends(get_sync_session),
                         user: User = Depends(current_user)):
    try:
        product = session.query(Product).where(Product.id== product_id).first() # ловим ошибку если товара нет
        user = session.query(User).where(User.id == user.id).first()
        if count >= user.cart[product.name]:
            del user.cart[product.name]
        else:
            user.cart[product.name] -= count
        session.add(user)
        session.commit()
        return {
            'status': 'successful'
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'not found {product.name}')