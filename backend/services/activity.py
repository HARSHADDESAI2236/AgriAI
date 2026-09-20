from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Activity, Crop, Season, Field, Farm
from schema import CreateActivity, UpdateActivity


async def create_activity(
    db: AsyncSession,
    activity: CreateActivity,
    user_id: int
):
    result = await db.execute(
        select(Crop)
        .join(Season, Crop.season_id == Season.id)
        .join(Field, Season.field_id == Field.id)
        .join(Farm, Field.farm_id == Farm.id)
        .where(
            Crop.id == activity.crop_id,
            Farm.user_id == user_id
        )
    )

    crop = result.scalar_one_or_none()

    if crop is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Crop Not Found!"
        )

    new_activity = Activity(
        crop_id=activity.crop_id,
        activity_type=activity.activity_type,
        activity_date=activity.activity_date,
        description=activity.description
    )

    db.add(new_activity)

    await db.commit()
    await db.refresh(new_activity)

    return new_activity


async def get_activities(
    db: AsyncSession,
    crop_id: int,
    user_id: int
):
    result = await db.execute(
        select(Activity)
        .join(Crop, Activity.crop_id == Crop.id)
        .join(Season, Crop.season_id == Season.id)
        .join(Field, Season.field_id == Field.id)
        .join(Farm, Field.farm_id == Farm.id)
        .where(
            Activity.crop_id == crop_id,
            Farm.user_id == user_id
        )
        .order_by(Activity.activity_date)
    )

    return result.scalars().all()


async def get_activity(
    db: AsyncSession,
    activity_id: int,
    user_id: int
):
    result = await db.execute(
        select(Activity)
        .join(Crop, Activity.crop_id == Crop.id)
        .join(Season, Crop.season_id == Season.id)
        .join(Field, Season.field_id == Field.id)
        .join(Farm, Field.farm_id == Farm.id)
        .where(
            Activity.id == activity_id,
            Farm.user_id == user_id
        )
    )

    activity = result.scalar_one_or_none()

    if activity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity Not Found!"
        )

    return activity


async def update_activity(
    db: AsyncSession,
    activity_id: int,
    activity: UpdateActivity,
    user_id: int
):
    result = await db.execute(
        select(Activity)
        .join(Crop, Activity.crop_id == Crop.id)
        .join(Season, Crop.season_id == Season.id)
        .join(Field, Season.field_id == Field.id)
        .join(Farm, Field.farm_id == Farm.id)
        .where(
            Activity.id == activity_id,
            Farm.user_id == user_id
        )
    )

    db_activity = result.scalar_one_or_none()

    if db_activity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity Not Found!"
        )

    if activity.activity_type is not None:
        db_activity.activity_type = activity.activity_type

    if activity.activity_date is not None:
        db_activity.activity_date = activity.activity_date

    if activity.description is not None:
        db_activity.description = activity.description

    await db.commit()
    await db.refresh(db_activity)

    return db_activity


async def delete_activity(
    db: AsyncSession,
    activity_id: int,
    user_id: int
):
    result = await db.execute(
        select(Activity)
        .join(Crop, Activity.crop_id == Crop.id)
        .join(Season, Crop.season_id == Season.id)
        .join(Field, Season.field_id == Field.id)
        .join(Farm, Field.farm_id == Farm.id)
        .where(
            Activity.id == activity_id,
            Farm.user_id == user_id
        )
    )

    db_activity = result.scalar_one_or_none()

    if db_activity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity Not Found!"
        )

    await db.delete(db_activity)
    await db.commit()

    return {
        "detail": "Activity deleted successfully!"
    }