from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from slugify import slugify
from sqlalchemy import select, insert
from sqlalchemy.orm import Session
from starlette import status

from app.backend.db_depends import get_db
from app.models import Product, Category
from app.schemas import CreateProduct

router = APIRouter(prefix='/products', tags=['products'])


@router.get('/')
async def all_products(db: Annotated[Session, Depends(get_db)]):
    products = db.scalars(select(Product).where(Product.is_active == True and Product.stock == 0)).all()
    if products is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There are no products")
    return products


@router.post('/create')
async def create_product(db: Annotated[Session, Depends(get_db)], product: CreateProduct):
    query = insert(Product).values(
        name=product.name,
        slug=slugify(product.name),
        description=product.description,
        price=product.price,
        image_url=product.image_url,
        stock=product.stock,
        category_id=product.category
    )

    db.execute(query)
    db.commit()

    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}


@router.get('/{category_slug}')
async def product_by_category(category_slug: str, db: Annotated[Session, Depends(get_db)]):

    chosen_category_id = db.scalar(select(Category.id).where(Category.slug == category_slug))
    if chosen_category_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There are no such category")

    subcategories = db.scalars(select(Category.id).where(Category.parent_id == chosen_category_id)).all()

    subcategories += [chosen_category_id]

    products = db.scalars(select(Product).where(Product.stock > 0 and
                                                Product.is_active == True and
                                                Product.category_id.in_(subcategories))).all()
    return products


@router.get('/detail/{product_slug}')
async def product_detail(product_slug: str):
    pass


@router.put('/detail/{product_slug}')
async def update_product(product_slug: str):
    pass


@router.delete('/delete')
async def delete_product(product_id: int):
    pass