from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from slugify import slugify
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from starlette import status

from app.backend.db_depends import get_db
from app.models import Category
from app.routes.auth import get_current_user
from app.schemas import CreateCategory

router = APIRouter(prefix="/category", tags=["category"])


@router.get("/all_categories")
async def get_all_categories(db: Annotated[AsyncSession, Depends(get_db)]):
    categories = await db.scalars(select(Category).where(Category.is_active == True))
    return categories.all()


@router.post("/create_category")
async def create_category(
    db: Annotated[AsyncSession, Depends(get_db)],
    category: CreateCategory,
    get_user: Annotated[dict, Depends(get_current_user)],
):
    if get_user.get("is_admin"):
        query = insert(Category).values(
            name=category.name,
            parent_id=category.parent_id,
            slug=slugify(category.name),
        )
        await db.execute(query)
        await db.commit()
        return {"status_code": status.HTTP_201_CREATED, "transaction": "Successful"}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="You must be admin user for this",
    )


@router.put("/update_category")
async def update_category(
    db: Annotated[AsyncSession, Depends(get_db)],
    category_id: int,
    category_update: CreateCategory,
    get_user: Annotated[dict, Depends(get_current_user)],
):
    if get_user.get("is_admin"):
        category = await db.scalar(select(Category).where(Category.id == category_id))

        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="There is no category found"
            )

        await db.execute(
            update(Category)
            .where(Category.id == category_id)
            .values(name=category_update.name, parent_id=category_update.parent_id)
        )
        await db.commit()
        return {
            "status_code": status.HTTP_200_OK,
            "transaction": "Category update is successful",
        }

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="You must be admin user for this",
    )


@router.delete("/delete_category")
async def delete_category(
    db: Annotated[AsyncSession, Depends(get_db)],
        category_id: int,
        get_user: Annotated[dict, Depends(get_current_user)]
):

    if get_user.get('is_admin'):
        category = await db.scalar(select(Category).where(Category.id == category_id))

        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="There is no category found"
            )
        query = update(Category).where(Category.id == category_id).values(is_active=False)
        await db.execute(query)
        await db.commit()
        return {
            "status_code": status.HTTP_200_OK,
            "transaction": "Category delete is successful",
        }

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="You must be admin user for this",
    )
