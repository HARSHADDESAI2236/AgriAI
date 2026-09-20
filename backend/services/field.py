from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Field, Farm
from schema import CreateField, UpdateField


async def create_field(
    db: AsyncSession,
    field: CreateField,
    user_id: int
):
    result = await db.execute(
        select(Farm).where(
            Farm.id == field.farm_id,
            Farm.user_id == user_id
        )
    )

    farm = result.scalar_one_or_none()

    if farm is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farm Not Found!"
        )

    new_field = Field(
        farm_id=field.farm_id,
        name=field.name,
        area=field.area
    )

    db.add(new_field)
    await db.commit()
    await db.refresh(new_field)

    return new_field


# =========================
# GET ALL FIELDS OF A FARM
# =========================

async def get_fields(
    db: AsyncSession,
    farm_id: int,
    user_id: int
):
    result = await db.execute(
        select(Field)
        .join(Farm, Field.farm_id == Farm.id)
        .where(
            Field.farm_id == farm_id,
            Farm.user_id == user_id
        )
    )

    return result.scalars().all()


# =========================
# GET SINGLE FIELD
# =========================

async def get_field(
    db: AsyncSession,
    field_id: int,
    user_id: int
):
    result = await db.execute(
        select(Field)
        .join(Farm, Field.farm_id == Farm.id)
        .where(
            Field.id == field_id,
            Farm.user_id == user_id
        )
    )

    field = result.scalar_one_or_none()

    if field is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Field Not Found!"
        )

    return field


# =========================
# UPDATE FIELD
# =========================

async def update_field(
    db: AsyncSession,
    field_id: int,
    field: UpdateField,
    user_id: int
):
    result = await db.execute(
        select(Field)
        .join(Farm, Field.farm_id == Farm.id)
        .where(
            Field.id == field_id,
            Farm.user_id == user_id
        )
    )

    db_field = result.scalar_one_or_none()

    if db_field is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Field Not Found!"
        )

    if field.name is not None:
        db_field.name = field.name

    if field.area is not None:
        db_field.area = field.area

    await db.commit()
    await db.refresh(db_field)

    return db_field


# =========================
# DELETE FIELD
# =========================

async def delete_field(
    db: AsyncSession,
    field_id: int,
    user_id: int
):
    result = await db.execute(
        select(Field)
        .join(Farm, Field.farm_id == Farm.id)
        .where(
            Field.id == field_id,
            Farm.user_id == user_id
        )
    )

    db_field = result.scalar_one_or_none()

    if db_field is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Field Not Found!"
        )

    await db.delete(db_field)
    await db.commit()

    return {
        "detail": "Field deleted successfully!"
    }