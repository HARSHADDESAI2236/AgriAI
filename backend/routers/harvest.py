from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from dependency import get_current_user
from models import User
from schema import CreateHarvest, HarvestResponse, UpdateHarvest

from services.harvest import (
    create_harvest,
    get_harvests,
    get_harvest,
    update_harvest,
    delete_harvest
)


router = APIRouter(
    prefix="/harvests",
    tags=["Harvests"]
)


@router.post("/", response_model=HarvestResponse)
async def create(
    harvest: CreateHarvest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await create_harvest(
        db,
        harvest,
        current_user.id
    )


@router.get(
    "/crop/{crop_id}",
    response_model=list[HarvestResponse]
)
async def get_all(
    crop_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await get_harvests(
        db,
        crop_id,
        current_user.id
    )


@router.get(
    "/{harvest_id}",
    response_model=HarvestResponse
)
async def get_one(
    harvest_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await get_harvest(
        db,
        harvest_id,
        current_user.id
    )


@router.put(
    "/{harvest_id}",
    response_model=HarvestResponse
)
async def update(
    harvest_id: int,
    harvest: UpdateHarvest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await update_harvest(
        db,
        harvest_id,
        harvest,
        current_user.id
    )


@router.delete("/{harvest_id}")
async def delete(
    harvest_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await delete_harvest(
        db,
        harvest_id,
        current_user.id
    )