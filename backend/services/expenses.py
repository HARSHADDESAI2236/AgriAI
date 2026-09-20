from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Expense, Crop, Season, Field, Farm
from schema import CreateExpense, UpdateExpense


async def create_expense(
    db: AsyncSession,
    expense: CreateExpense,
    user_id: int
):
    result = await db.execute(
        select(Crop)
        .join(Season, Crop.season_id == Season.id)
        .join(Field, Season.field_id == Field.id)
        .join(Farm, Field.farm_id == Farm.id)
        .where(
            Crop.id == expense.crop_id,
            Farm.user_id == user_id
        )
    )

    crop = result.scalar_one_or_none()

    if crop is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Crop Not Found!"
        )

    new_expense = Expense(
        crop_id=expense.crop_id,
        expense_type=expense.expense_type,
        amount=expense.amount,
        expense_date=expense.expense_date,
        description=expense.description
    )

    db.add(new_expense)

    await db.commit()
    await db.refresh(new_expense)

    return new_expense


async def get_expenses(
    db: AsyncSession,
    crop_id: int,
    user_id: int
):
    result = await db.execute(
        select(Expense)
        .join(Crop, Expense.crop_id == Crop.id)
        .join(Season, Crop.season_id == Season.id)
        .join(Field, Season.field_id == Field.id)
        .join(Farm, Field.farm_id == Farm.id)
        .where(
            Expense.crop_id == crop_id,
            Farm.user_id == user_id
        )
        .order_by(Expense.expense_date)
    )

    return result.scalars().all()


async def get_expense(
    db: AsyncSession,
    expense_id: int,
    user_id: int
):
    result = await db.execute(
        select(Expense)
        .join(Crop, Expense.crop_id == Crop.id)
        .join(Season, Crop.season_id == Season.id)
        .join(Field, Season.field_id == Field.id)
        .join(Farm, Field.farm_id == Farm.id)
        .where(
            Expense.id == expense_id,
            Farm.user_id == user_id
        )
    )

    expense = result.scalar_one_or_none()

    if expense is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense Not Found!"
        )

    return expense


async def update_expense(
    db: AsyncSession,
    expense_id: int,
    expense: UpdateExpense,
    user_id: int
):
    result = await db.execute(
        select(Expense)
        .join(Crop, Expense.crop_id == Crop.id)
        .join(Season, Crop.season_id == Season.id)
        .join(Field, Season.field_id == Field.id)
        .join(Farm, Field.farm_id == Farm.id)
        .where(
            Expense.id == expense_id,
            Farm.user_id == user_id
        )
    )

    db_expense = result.scalar_one_or_none()

    if db_expense is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense Not Found!"
        )

    if expense.expense_type is not None:
        db_expense.expense_type = expense.expense_type

    if expense.amount is not None:
        db_expense.amount = expense.amount

    if expense.expense_date is not None:
        db_expense.expense_date = expense.expense_date

    if expense.description is not None:
        db_expense.description = expense.description

    await db.commit()
    await db.refresh(db_expense)

    return db_expense


async def delete_expense(
    db: AsyncSession,
    expense_id: int,
    user_id: int
):
    result = await db.execute(
        select(Expense)
        .join(Crop, Expense.crop_id == Crop.id)
        .join(Season, Crop.season_id == Season.id)
        .join(Field, Season.field_id == Field.id)
        .join(Farm, Field.farm_id == Farm.id)
        .where(
            Expense.id == expense_id,
            Farm.user_id == user_id
        )
    )

    db_expense = result.scalar_one_or_none()

    if db_expense is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense Not Found!"
        )

    await db.delete(db_expense)
    await db.commit()

    return {
        "detail": "Expense deleted successfully!"
    }