from fastapi import APIRouter, Depends,Query
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from dependency import get_current_user
from models import User
from schema import CropHistoryResponse,FarmHistoryResponse

from services.history import get_crop_history,get_farm_history


router = APIRouter(
    prefix="/history",
    tags=["Farm History"]
)


@router.get(
    "/crop/{crop_id}",
    response_model=CropHistoryResponse
)
async def crop_history(
    crop_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await get_crop_history(
        db,
        crop_id,
        current_user.id
    )


@router.get("/", response_model=FarmHistoryResponse)
async def farm_history(
    field_id: int | None = Query(default=None),
    season_id: int | None = Query(default=None),
    crop_id: int | None = Query(default=None),
    record_type: str | None = Query(default=None),

    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    records = await get_farm_history(
        db=db,
        user_id=current_user.id,
        field_id=field_id,
        season_id=season_id,
        crop_id=crop_id,
        record_type=record_type,
    )

    return {
        "records": records
    }