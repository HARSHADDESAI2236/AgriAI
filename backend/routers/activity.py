from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from dependency import get_current_user
from models import User
from schema import CreateActivity, ActivityResponse, UpdateActivity

from services.activity import (
    create_activity,
    get_activities,
    get_activity,
    update_activity,
    delete_activity
)


router = APIRouter(
    prefix="/activities",
    tags=["Activities"]
)


@router.post("/", response_model=ActivityResponse)
async def create_activity_route(
    activity: CreateActivity,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await create_activity(
        db=db,
        activity=activity,
        user_id=int(current_user.id)
    )


@router.get("/crop/{crop_id}", response_model=list[ActivityResponse])
async def get_activities_route(
    crop_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await get_activities(
        db=db,
        crop_id=crop_id,
        user_id=int(current_user.id)
    )


@router.get("/{activity_id}", response_model=ActivityResponse)
async def get_activity_route(
    activity_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await get_activity(
        db=db,
        activity_id=activity_id,
        user_id=int(current_user.id)
    )


@router.put("/{activity_id}", response_model=ActivityResponse)
async def update_activity_route(
    activity_id: int,
    activity: UpdateActivity,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await update_activity(
        db=db,
        activity_id=activity_id,
        activity=activity,
        user_id=int(current_user.id)
    )


@router.delete("/{activity_id}")
async def delete_activity_route(
    activity_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await delete_activity(
        db=db,
        activity_id=activity_id,
        user_id=int(current_user.id)
    )