from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Input, Crop, Season, Field, Farm
from schema import CreateInput, UpdateInput


async def create_input(
    db: AsyncSession,
    input_data: CreateInput,
    user_id: int
):
    result = await db.execute(
        select(Crop)
        .join(Season, Crop.season_id == Season.id)
        .join(Field, Season.field_id == Field.id)
        .join(Farm, Field.farm_id == Farm.id)
        .where(
            Crop.id == input_data.crop_id,
            Farm.user_id == user_id
        )
    )

    crop = result.scalar_one_or_none()

    if crop is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Crop Not Found!"
        )

    new_input = Input(
        crop_id=input_data.crop_id,
        input_name=input_data.input_name,
        input_type=input_data.input_type,
        quantity=input_data.quantity,
        unit=input_data.unit,
        application_date=input_data.application_date,
        cost=input_data.cost,
        description=input_data.description
    )

    db.add(new_input)

    await db.commit()
    await db.refresh(new_input)

    return new_input


async def get_inputs(
    db: AsyncSession,
    crop_id: int,
    user_id: int
):
    result = await db.execute(
        select(Input)
        .join(Crop, Input.crop_id == Crop.id)
        .join(Season, Crop.season_id == Season.id)
        .join(Field, Season.field_id == Field.id)
        .join(Farm, Field.farm_id == Farm.id)
        .where(
            Input.crop_id == crop_id,
            Farm.user_id == user_id
        )
        .order_by(Input.application_date)
    )

    return result.scalars().all()


async def get_input(
    db: AsyncSession,
    input_id: int,
    user_id: int
):
    result = await db.execute(
        select(Input)
        .join(Crop, Input.crop_id == Crop.id)
        .join(Season, Crop.season_id == Season.id)
        .join(Field, Season.field_id == Field.id)
        .join(Farm, Field.farm_id == Farm.id)
        .where(
            Input.id == input_id,
            Farm.user_id == user_id
        )
    )

    input_record = result.scalar_one_or_none()

    if input_record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Input Not Found!"
        )

    return input_record


async def update_input(
    db: AsyncSession,
    input_id: int,
    input_data: UpdateInput,
    user_id: int
):
    result = await db.execute(
        select(Input)
        .join(Crop, Input.crop_id == Crop.id)
        .join(Season, Crop.season_id == Season.id)
        .join(Field, Season.field_id == Field.id)
        .join(Farm, Field.farm_id == Farm.id)
        .where(
            Input.id == input_id,
            Farm.user_id == user_id
        )
    )

    db_input = result.scalar_one_or_none()

    if db_input is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Input Not Found!"
        )

    if input_data.input_name is not None:
        db_input.input_name = input_data.input_name

    if input_data.input_type is not None:
        db_input.input_type = input_data.input_type

    if input_data.quantity is not None:
        db_input.quantity = input_data.quantity

    if input_data.unit is not None:
        db_input.unit = input_data.unit

    if input_data.application_date is not None:
        db_input.application_date = input_data.application_date

    if input_data.cost is not None:
        db_input.cost = input_data.cost

    if input_data.description is not None:
        db_input.description = input_data.description

    await db.commit()
    await db.refresh(db_input)

    return db_input


async def delete_input(
    db: AsyncSession,
    input_id: int,
    user_id: int
):
    result = await db.execute(
        select(Input)
        .join(Crop, Input.crop_id == Crop.id)
        .join(Season, Crop.season_id == Season.id)
        .join(Field, Season.field_id == Field.id)
        .join(Farm, Field.farm_id == Farm.id)
        .where(
            Input.id == input_id,
            Farm.user_id == user_id
        )
    )

    db_input = result.scalar_one_or_none()

    if db_input is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Input Not Found!"
        )

    await db.delete(db_input)
    await db.commit()

    return {
        "detail": "Input deleted successfully!"
    }