from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.backend.db_depends import get_db
from app.models.user import User
from app.routes.auth import get_current_user

router = APIRouter(prefix='/permission', tags=['permission'])


@router.patch('/')
async def supplier_permission(db: Annotated[AsyncSession, Depends(get_db)], get_user: Annotated[dict, Depends(get_current_user)],
                              user_id: int):
    if get_user.get('is_admin'):
        user = await db.scalar(select(User).where(User.id == user_id))

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No user with id {user_id}"
            )

        if user.is_supplier:
            query = update(User).where(User.id == user_id).values(is_supplier=False, is_customer=True)
        else:
            query = update(User).where(User.id == user_id).values(is_supplier=True, is_customer=False)

        await db.execute(query)
        await db.commit()
        return {
            "status": status.HTTP_200_OK,
            "transaction": "successful"
        }

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You haven't enough permission")


@router.patch('/delete')
async def delete_user(db: Annotated[AsyncSession, Depends(get_db)], get_user: Annotated[dict, Depends(get_current_user)],
                              user_id: int):
    if get_user.get('is_admin'):
        user = await db.scalar(select(User).where(User.id == user_id))

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No user with id {user_id}"
            )

        if user.is_active:
            query = update(User).where(User.id == user_id).values(is_active=False)
        else:
            query = update(User).where(User.id == user_id).values(is_active=True)

        await db.execute(query)
        await db.commit()
        return {
            "status": status.HTTP_200_OK,
            "transaction": "successful"
        }

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You haven't enough permission")