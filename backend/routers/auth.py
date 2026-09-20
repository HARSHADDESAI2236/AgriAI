
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from models import User
from database import get_db
from dependency import get_current_user
from schema import CreateUser, UserResponse, LoginUser, UpdateUser

from services.user import (
    create_user,
    verify_user,
    update_user,
    delete_user
)


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# =========================
# CREATE USER
# =========================

@router.post(
    "/",
    response_model=UserResponse
)
async def register_user(
    user: CreateUser,
    db: AsyncSession = Depends(get_db)
   
):
    return await create_user(db, user)


# =========================
# LOGIN
# =========================

@router.post("/login")
async def login_user(
    user: LoginUser,
    db: AsyncSession = Depends(get_db)
):
    return await verify_user(
        db=db,
        email=user.email,
        password=user.password
    )


# =========================
# UPDATE USER
# =========================

@router.put(
    "/{user_id}",
    response_model=UserResponse
)
async def update_user_route(
    user_id: int,
    user: UpdateUser,
    current_user:User=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await update_user(
        db=db,
        user=user,
        user_id=user_id
    )


# =========================
# DELETE USER
# =========================

@router.delete("/{user_id}")
async def delete_user_route(
    user_id: int,
    current_user:User=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await delete_user(
        db=db,
        user_id=user_id
    )


@router.post("/token")
async def login_for_swagger(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    return await verify_user(
        db=db,
        email=form_data.username,
        password=form_data.password
    )