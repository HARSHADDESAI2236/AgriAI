from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Crop, Season, Field, Farm
from schema import CreateCrop, UpdateCrop


async def create_crop(
    db: AsyncSession,
    crop: CreateCrop,
    user_id: int
):
    result = await db.execute(
        select(Season)
        .join(Field, Season.field_id == Field.id)
        .join(Farm, Field.farm_id == Farm.id)
        .where(
            Season.id == crop.season_id,
            Farm.user_id == user_id
        )
    )

    season = result.scalar_one_or_none()

    if season is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Season Not Found!"
        )

    new_crop = Crop(
        season_id=crop.season_id,
        name=crop.name,
        variety=crop.variety,
        sowing_date=crop.sowing_date,
        harvest_date=crop.harvest_date
    )

    db.add(new_crop)
    await db.commit()
    await db.refresh(new_crop)

    return new_crop


async def get_crops(
    db: AsyncSession,
    season_id: int,
    user_id: int
):
    result = await db.execute(
        select(Crop)
        .join(Season, Crop.season_id == Season.id)
        .join(Field, Season.field_id == Field.id)
        .join(Farm, Field.farm_id == Farm.id)
        .where(
            Crop.season_id == season_id,
            Farm.user_id == user_id
        )
        .order_by(Crop.sowing_date)
    )

    return result.scalars().all()


async def get_crop(
    db: AsyncSession,
    crop_id: int,
    user_id: int
):
    result = await db.execute(
        select(Crop)
        .join(Season, Crop.season_id == Season.id)
        .join(Field, Season.field_id == Field.id)
        .join(Farm, Field.farm_id == Farm.id)
        .where(
            Crop.id == crop_id,
            Farm.user_id == user_id
        )
    )

    crop = result.scalar_one_or_none()

    if crop is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Crop Not Found!"
        )

    return crop


async def update_crop(
    db: AsyncSession,
    crop_id: int,
    crop: UpdateCrop,
    user_id: int
):
    result = await db.execute(
        select(Crop)
        .join(Season, Crop.season_id == Season.id)
        .join(Field, Season.field_id == Field.id)
        .join(Farm, Field.farm_id == Farm.id)
        .where(
            Crop.id == crop_id,
            Farm.user_id == user_id
        )
    )

    db_crop = result.scalar_one_or_none()

    if db_crop is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Crop Not Found!"
        )

    if crop.name is not None:
        db_crop.name = crop.name

    if crop.variety is not None:
        db_crop.variety = crop.variety

    if crop.sowing_date is not None:
        db_crop.sowing_date = crop.sowing_date

    if crop.harvest_date is not None:
        db_crop.harvest_date = crop.harvest_date

    await db.commit()
    await db.refresh(db_crop)

    return db_crop


async def delete_crop(
    db: AsyncSession,
    crop_id: int,
    user_id: int
):
    result = await db.execute(
        select(Crop)
        .join(Season, Crop.season_id == Season.id)
        .join(Field, Season.field_id == Field.id)
        .join(Farm, Field.farm_id == Farm.id)
        .where(
            Crop.id == crop_id,
            Farm.user_id == user_id
        )
    )

    db_crop = result.scalar_one_or_none()

    if db_crop is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Crop Not Found!"
        )

    await db.delete(db_crop)
    await db.commit()

    return {"detail": "Crop deleted successfully!"}