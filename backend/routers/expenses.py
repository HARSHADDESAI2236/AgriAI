from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from dependency import get_current_user
from models import User
from schema import CreateExpense, ExpenseResponse, UpdateExpense

from services.expenses import (
    create_expense,
    get_expenses,
    get_expense,
    update_expense,
    delete_expense
)


router = APIRouter(
    prefix="/expenses",
    tags=["Expenses"]
)


@router.post("/", response_model=ExpenseResponse)
async def create(
    expense: CreateExpense,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await create_expense(
        db,
        expense,
        current_user.id
    )


@router.get(
    "/crop/{crop_id}",
    response_model=list[ExpenseResponse]
)
async def get_all(
    crop_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await get_expenses(
        db,
        crop_id,
        current_user.id
    )


@router.get(
    "/{expense_id}",
    response_model=ExpenseResponse
)
async def get_one(
    expense_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await get_expense(
        db,
        expense_id,
        current_user.id
    )


@router.put(
    "/{expense_id}",
    response_model=ExpenseResponse
)
async def update(
    expense_id: int,
    expense: UpdateExpense,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await update_expense(
        db,
        expense_id,
        expense,
        current_user.id
    )


@router.delete("/{expense_id}")
async def delete(
    expense_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await delete_expense(
        db,
        expense_id,
        current_user.id
    )