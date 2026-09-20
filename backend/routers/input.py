from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from dependency import get_current_user
from models import User
from schema import CreateInput, InputResponse, UpdateInput

from services.input  import (
    create_input,
    get_inputs,
    get_input,
    update_input,
    delete_input
)


router = APIRouter(
    prefix="/inputs",
    tags=["Inputs"]
)


@router.post("/", response_model=InputResponse)
async def create(
    input_data: CreateInput,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await create_input(
        db,
        input_data,
        current_user.id
    )


@router.get(
    "/crop/{crop_id}",
    response_model=list[InputResponse]
)
async def get_all(
    crop_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await get_inputs(
        db,
        crop_id,
        current_user.id
    )


@router.get(
    "/{input_id}",
    response_model=InputResponse
)
async def get_one(
    input_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await get_input(
        db,
        input_id,
        current_user.id
    )


@router.put(
    "/{input_id}",
    response_model=InputResponse
)
async def update(
    input_id: int,
    input_data: UpdateInput,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await update_input(
        db,
        input_id,
        input_data,
        current_user.id
    )


@router.delete("/{input_id}")
async def delete(
    input_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await delete_input(
        db,
        input_id,
        current_user.id
    )