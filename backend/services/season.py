from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Season, Field, Farm
from schema import CreateSeason, UpdateSeason


async def create_season(
    db: AsyncSession,
    season: CreateSeason,
    user_id: int
):
    result = await db.execute(
        select(Field)
        .join(Farm, Field.farm_id == Farm.id)
        .where(
            Field.id == season.field_id,
            Farm.user_id == user_id
        )
    )

    field = result.scalar_one_or_none()

    if field is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Field Not Found!"
        )

    new_season = Season(
        field_id=season.field_id,
        name=season.name,
        start_date=season.start_date,
        end_date=season.end_date
    )

    db.add(new_season)

    await db.commit()
    await db.refresh(new_season)

    return new_season


async def get_seasons(
    db: AsyncSession,
    field_id: int,
    user_id: int
):
    result = await db.execute(
        select(Season)
        .join(Field, Season.field_id == Field.id)
        .join(Farm, Field.farm_id == Farm.id)
        .where(
            Season.field_id == field_id,
            Farm.user_id == user_id
        )
        .order_by(Season.start_date)
    )

    return result.scalars().all()


async def get_season(
    db: AsyncSession,
    season_id: int,
    user_id: int
):
    result = await db.execute(
        select(Season)
        .join(Field, Season.field_id == Field.id)
        .join(Farm, Field.farm_id == Farm.id)
        .where(
            Season.id == season_id,
            Farm.user_id == user_id
        )
    )

    season = result.scalar_one_or_none()

    if season is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Season Not Found!"
        )

    return season


async def update_season(
    db: AsyncSession,
    season_id: int,
    season: UpdateSeason,
    user_id: int
):
    result = await db.execute(
        select(Season)
        .join(Field, Season.field_id == Field.id)
        .join(Farm, Field.farm_id == Farm.id)
        .where(
            Season.id == season_id,
            Farm.user_id == user_id
        )
    )

    db_season = result.scalar_one_or_none()

    if db_season is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Season Not Found!"
        )

    if season.name is not None:
        db_season.name = season.name

    if season.start_date is not None:
        db_season.start_date = season.start_date

    if season.end_date is not None:
        db_season.end_date = season.end_date

    await db.commit()
    await db.refresh(db_season)

    return db_season


async def delete_season(
    db: AsyncSession,
    season_id: int,
    user_id: int
):
    result = await db.execute(
        select(Season)
        .join(Field, Season.field_id == Field.id)
        .join(Farm, Field.farm_id == Farm.id)
        .where(
            Season.id == season_id,
            Farm.user_id == user_id
        )
    )

    db_season = result.scalar_one_or_none()

    if db_season is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Season Not Found!"
        )

    await db.delete(db_season)
    await db.commit()

    return {
        "detail": "Season deleted successfully!"
    }