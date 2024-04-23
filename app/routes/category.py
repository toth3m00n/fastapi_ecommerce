from typing import Annotated

from fastapi import APIRouter, Depends
from slugify import slugify
from sqlalchemy import insert
from sqlalchemy.orm import Session
from starlette import status

from app.backend.db_depends import get_db
from app.models import Category
from app.schemas import CreateCategory

router = APIRouter(prefix='/category', tags=['category'])


@router.get('/all_categories')
async def get_all_categories():
    pass


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
async def update_category():
    pass


@router.delete('/delete_category')
async def delete_category():
    pass
