from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from slugify import slugify
from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from starlette import status

from app.backend.db_depends import get_db
from app.models import Product, Category
from app.routes.auth import get_current_user
from app.schemas import CreateProduct

router = APIRouter(prefix='/products', tags=['products'])


@router.get('/')
async def all_products(db: Annotated[AsyncSession, Depends(get_db)]):
    products = await db.scalars(select(Product).where(Product.is_active == True, Product.stock >= 0))
    if products is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There are no products")
    return products.all()


@router.post('/create')
async def create_product(db: Annotated[AsyncSession, Depends(get_db)],
                         product: CreateProduct,
                         get_user: Annotated[dict, Depends(get_current_user)]):
    if get_user.get('is_admin') or get_user.get('is_supplier'):

        query = insert(Product).values(
            name=product.name,
            slug=slugify(product.name),
            description=product.description,
            price=product.price,
            image_url=product.image_url,
            stock=product.stock,
            category_id=product.category,
            supplier_id=get_user.get('id')
        )

        await db.execute(query)
        await db.commit()

        return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='You are not authorized to use this method'
    )


@router.get('/{category_slug}')
async def product_by_category(category_slug: str, db: Annotated[AsyncSession, Depends(get_db)]):

    chosen_category_id = await db.scalar(select(Category.id).where(Category.slug == category_slug))
    if chosen_category_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There are no such category")

    subcategories = await db.scalars(select(Category.id).where(Category.parent_id == chosen_category_id))

    subcategories = subcategories.all() + [chosen_category_id]
    products = await db.scalars(select(Product).where(Product.stock >= 0,
                                                Product.is_active == True,
                                                Product.category_id.in_(subcategories)))
    return products.all()


@router.get('/detail/{product_slug}')
async def product_detail(product_slug: str, db: Annotated[AsyncSession, Depends(get_db)]):
    current_product = await db.scalar(select(Product).where(Product.slug == product_slug, Product.stock >= 0))
    if current_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no such product with slug {}".format(product_slug)
        )
    return current_product


@router.put('/detail/{product_slug}')
async def update_product(product_slug: str, db: Annotated[AsyncSession, Depends(get_db)], product_update: CreateProduct,
                         get_user: Annotated[dict, Depends(get_current_user)]):
    current_product = await db.scalar(select(Product).where(Product.slug == product_slug))
    if current_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no such product with slug {}".format(product_slug)
        )

    if get_user.get('is_supplier') or get_user.get('is_admin'):

        if get_user.get('id') == product_update.supplier_id or get_user.get('is_admin'):
            query = update(Product).where(Product.slug == product_slug).values(
                name=product_update.name,
                description=product_update.description,
                price=product_update.price,
                image_url=product_update.image_url,
                stock=product_update.stock,
                category_id=product_update.category
            )

            await db.execute(query)
            await db.commit()
            return {
                'status_code': status.HTTP_200_OK,
                'transaction': 'Product update is successful'
            }

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='You are not authorized to use this method'
        )

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='You are not authorized to use this method'
    )


@router.delete('/delete')
async def delete_product(product_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    product = await db.scalar(select(Product).where(Product.id == product_id))

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There is no product found'
        )
    query = update(Product).where(Product.id == product_id).values(is_active=False)
    await db.execute(query)
    await db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Category delete is successful'
    }
