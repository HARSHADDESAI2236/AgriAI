from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from dependency import get_current_user
from models import User
from schema import CreateField, FieldResponse, UpdateField

from services.field import (
    create_field,
    get_fields,
    get_field,
    update_field,
    delete_field
)


router = APIRouter(
    prefix="/fields",
    tags=["Fields"]
)


# =========================
# CREATE FIELD
# =========================

@router.post(
    "/",
    response_model=FieldResponse
)
async def create_field_route(
    field: CreateField,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await create_field(
        db=db,
        field=field,
        user_id=int(current_user.id)
    )


# =========================
# GET ALL FIELDS OF FARM
# =========================

@router.get(
    "/farm/{farm_id}",
    response_model=list[FieldResponse]
)
async def get_fields_route(
    farm_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await get_fields(
        db=db,
        farm_id=farm_id,
        user_id=int(current_user.id)
    )


# =========================
# GET SINGLE FIELD
# =========================

@router.get(
    "/{field_id}",
    response_model=FieldResponse
)
async def get_field_route(
    field_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await get_field(
        db=db,
        field_id=field_id,
        user_id=int(current_user.id)
    )


# =========================
# UPDATE FIELD
# =========================

@router.put(
    "/{field_id}",
    response_model=FieldResponse
)
async def update_field_route(
    field_id: int,
    field: UpdateField,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await update_field(
        db=db,
        field_id=field_id,
        field=field,
        user_id=int(current_user.id)
    )


# =========================
# DELETE FIELD
# =========================

@router.delete("/{field_id}")
async def delete_field_route(
    field_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await delete_field(
        db=db,
        field_id=field_id,
        user_id=int(current_user.id)
    )