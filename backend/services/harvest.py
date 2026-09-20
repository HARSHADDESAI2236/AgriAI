from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Harvest, Crop, Season, Field, Farm
from schema import CreateHarvest, UpdateHarvest


async def create_harvest(
    db: AsyncSession,
    harvest: CreateHarvest,
    user_id: int
):
    result = await db.execute(
        select(Crop)
        .join(Season, Crop.season_id == Season.id)
        .join(Field, Season.field_id == Field.id)
        .join(Farm, Field.farm_id == Farm.id)
        .where(
            Crop.id == harvest.crop_id,
            Farm.user_id == user_id
        )
    )

    crop = result.scalar_one_or_none()

    if crop is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Crop Not Found!"
        )

    new_harvest = Harvest(
        crop_id=harvest.crop_id,
        harvest_date=harvest.harvest_date,
        quantity=harvest.quantity,
        unit=harvest.unit,
        selling_price=harvest.selling_price,
        description=harvest.description
    )

    db.add(new_harvest)

    await db.commit()
    await db.refresh(new_harvest)

    return new_harvest


async def get_harvests(
    db: AsyncSession,
    crop_id: int,
    user_id: int
):
    result = await db.execute(
        select(Harvest)
        .join(Crop, Harvest.crop_id == Crop.id)
        .join(Season, Crop.season_id == Season.id)
        .join(Field, Season.field_id == Field.id)
        .join(Farm, Field.farm_id == Farm.id)
        .where(
            Harvest.crop_id == crop_id,
            Farm.user_id == user_id
        )
        .order_by(Harvest.harvest_date)
    )

    return result.scalars().all()


async def get_harvest(
    db: AsyncSession,
    harvest_id: int,
    user_id: int
):
    result = await db.execute(
        select(Harvest)
        .join(Crop, Harvest.crop_id == Crop.id)
        .join(Season, Crop.season_id == Season.id)
        .join(Field, Season.field_id == Field.id)
        .join(Farm, Field.farm_id == Farm.id)
        .where(
            Harvest.id == harvest_id,
            Farm.user_id == user_id
        )
    )

    harvest = result.scalar_one_or_none()

    if harvest is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Harvest Not Found!"
        )

    return harvest


async def update_harvest(
    db: AsyncSession,
    harvest_id: int,
    harvest: UpdateHarvest,
    user_id: int
):
    result = await db.execute(
        select(Harvest)
        .join(Crop, Harvest.crop_id == Crop.id)
        .join(Season, Crop.season_id == Season.id)
        .join(Field, Season.field_id == Field.id)
        .join(Farm, Field.farm_id == Farm.id)
        .where(
            Harvest.id == harvest_id,
            Farm.user_id == user_id
        )
    )

    db_harvest = result.scalar_one_or_none()

    if db_harvest is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Harvest Not Found!"
        )

    if harvest.harvest_date is not None:
        db_harvest.harvest_date = harvest.harvest_date

    if harvest.quantity is not None:
        db_harvest.quantity = harvest.quantity

    if harvest.unit is not None:
        db_harvest.unit = harvest.unit

    if harvest.selling_price is not None:
        db_harvest.selling_price = harvest.selling_price

    if harvest.description is not None:
        db_harvest.description = harvest.description

    await db.commit()
    await db.refresh(db_harvest)

    return db_harvest


async def delete_harvest(
    db: AsyncSession,
    harvest_id: int,
    user_id: int
):
    result = await db.execute(
        select(Harvest)
        .join(Crop, Harvest.crop_id == Crop.id)
        .join(Season, Crop.season_id == Season.id)
        .join(Field, Season.field_id == Field.id)
        .join(Farm, Field.farm_id == Farm.id)
        .where(
            Harvest.id == harvest_id,
            Farm.user_id == user_id
        )
    )

    db_harvest = result.scalar_one_or_none()

    if db_harvest is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Harvest Not Found!"
        )

    await db.delete(db_harvest)
    await db.commit()

    return {
        "detail": "Harvest deleted successfully!"
    }