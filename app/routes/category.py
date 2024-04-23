from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from slugify import slugify
from sqlalchemy import insert, select, update
from sqlalchemy.orm import Session
from starlette import status

from app.backend.db_depends import get_db
from app.models import Category
from app.schemas import CreateCategory

router = APIRouter(prefix='/category', tags=['category'])


@router.get('/all_categories')
async def get_all_categories(db: Annotated[Session, Depends(get_db)]):
    categories = db.scalars(select(Category).where(Category.is_active == True)).all()
    print(db.scalars(select(Category)))
    return categories


@router.post('/create_category')
async def create_category(db: Annotated[Session, Depends(get_db)], category: CreateCategory):
    query = insert(Category).values(
        name=category.name,
        parent_id=category.parent_id,
        slug=slugify(category.name)
    )
    db.execute(query)
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }


@router.put('/update_category')
async def update_category(db: Annotated[Session, Depends(get_db)], category_id: int, category_update: CreateCategory):
    category = db.scalar(select(Category).where(Category.id == category_id))

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There is no category found'
        )

    db.execute(update(Category).where(Category.id == category_id).values(name=category_update.name,
                                                                         parent_id=category_update.parent_id))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Category update is successful'
    }


@router.delete('/delete_category')
async def delete_category(db: Annotated[Session, Depends(get_db)], category_id: int):
    category = db.scalar(select(Category).where(Category.id == category_id))

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There is no category found'
        )
    query = update(Category).where(Category.id == category_id).values(is_active=False)
    db.execute(query)
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Category delete is successful'
    }
