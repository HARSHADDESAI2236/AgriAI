from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Farm
from schema import CreateFarm, UpdateFarm


async def create_farm(
    db: AsyncSession,
    farm: CreateFarm,
    user_id: int
):
    new_farm = Farm(
        user_id=user_id,
        name=farm.name,
        location=farm.location,
        total_area=farm.total_area,
        area_unit=farm.area_unit
    )

    db.add(new_farm)

    await db.commit()
    await db.refresh(new_farm)

    return new_farm


async def get_farms(
    db: AsyncSession,
    user_id: int
):
    result = await db.execute(
        select(Farm).where(Farm.user_id == user_id)
    )

    return result.scalars().all()


async def get_farm(
    db: AsyncSession,
    farm_id: int,
    user_id: int
):
    result = await db.execute(
        select(Farm).where(
            Farm.id == farm_id,
            Farm.user_id == user_id
        )
    )

    farm = result.scalar_one_or_none()

    if farm is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farm Not Found!"
        )

    return farm


async def update_farm(
    db: AsyncSession,
    farm_id: int,
    farm: UpdateFarm,
    user_id: int
):
    result = await db.execute(
        select(Farm).where(
            Farm.id == farm_id,
            Farm.user_id == user_id
        )
    )

    db_farm = result.scalar_one_or_none()

    if db_farm is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farm Not Found!"
        )

    if farm.name is not None:
        db_farm.name = farm.name

    if farm.location is not None:
        db_farm.location = farm.location

    if farm.total_area is not None:
        db_farm.total_area = farm.total_area

    if farm.area_unit is not None:
        db_farm.area_unit = farm.area_unit

    await db.commit()
    await db.refresh(db_farm)

    return db_farm


async def delete_farm(
    db: AsyncSession,
    farm_id: int,
    user_id: int
):
    result = await db.execute(
        select(Farm).where(
            Farm.id == farm_id,
            Farm.user_id == user_id
        )
    )

    db_farm = result.scalar_one_or_none()

    if db_farm is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farm Not Found!"
        )

    await db.delete(db_farm)
    await db.commit()

    return {
        "detail": "Farm deleted successfully!"
    }