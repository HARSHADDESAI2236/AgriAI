from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from dependency import get_current_user
from models import User
from schema import CreateCrop, CropResponse, UpdateCrop
from services.crop import (
    create_crop,
    get_crops,
    get_crop,
    update_crop,
    delete_crop
)

router = APIRouter(
    prefix="/crops",
    tags=["Crops"]
)


@router.post("/", response_model=CropResponse)
async def create(
    crop: CreateCrop,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await create_crop(db, crop, current_user.id)


@router.get("/season/{season_id}", response_model=list[CropResponse])
async def get_all(
    season_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await get_crops(db, season_id, current_user.id)


@router.get("/{crop_id}", response_model=CropResponse)
async def get_one(
    crop_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await get_crop(db, crop_id, current_user.id)


@router.put("/{crop_id}", response_model=CropResponse)
async def update(
    crop_id: int,
    crop: UpdateCrop,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await update_crop(
        db,
        crop_id,
        crop,
        current_user.id
    )


@router.delete("/{crop_id}")
async def delete(
    crop_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await delete_crop(
        db,
        crop_id,
        current_user.id
    )