from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from dependency import get_current_user

from models import User
from schema import CreateFarm, FarmResponse, UpdateFarm

from services.farm import (
    create_farm,
    get_farms,
    get_farm,
    update_farm,
    delete_farm
)


router = APIRouter(
    prefix="/farms",
    tags=["Farms"]
)


@router.post(
    "/",
    response_model=FarmResponse
)
async def create_farm_route(
    farm: CreateFarm,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await create_farm(
        db=db,
        farm=farm,
        user_id=current_user.id
    )


@router.get(
    "/",
    response_model=list[FarmResponse]
)
async def get_farms_route(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await get_farms(
        db=db,
        user_id=current_user.id
    )


@router.get(
    "/{farm_id}",
    response_model=FarmResponse
)
async def get_farm_route(
    farm_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await get_farm(
        db=db,
        farm_id=farm_id,
        user_id=current_user.id
    )


@router.put(
    "/{farm_id}",
    response_model=FarmResponse
)
async def update_farm_route(
    farm_id: int,
    farm: UpdateFarm,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await update_farm(
        db=db,
        farm_id=farm_id,
        farm=farm,
        user_id=current_user.id
    )


@router.delete(
    "/{farm_id}"
)
async def delete_farm_route(
    farm_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await delete_farm(
        db=db,
        farm_id=farm_id,
        user_id=current_user.id
    )