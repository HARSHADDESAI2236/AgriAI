from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from dependency import get_current_user
from models import User
from schema import CreateSeason, SeasonResponse, UpdateSeason

from services.season  import create_season,update_season,delete_season,get_season,get_seasons 



router = APIRouter(
    prefix="/seasons",
    tags=["Seasons"]
)


@router.post("/", response_model=SeasonResponse)
async def create_season_route(
    season: CreateSeason,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await create_season(
        db=db,
        season=season,
        user_id=int(current_user.id)
    )


@router.get("/field/{field_id}", response_model=list[SeasonResponse])
async def get_seasons_route(
    field_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await get_seasons(
        db=db,
        field_id=field_id,
        user_id=int(current_user.id)
    )


@router.get("/{season_id}", response_model=SeasonResponse)
async def get_season_route(
    season_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await get_season(
        db=db,
        season_id=season_id,
        user_id=int(current_user.id)
    )


@router.put("/{season_id}", response_model=SeasonResponse)
async def update_season_route(
    season_id: int,
    season: UpdateSeason,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await update_season(
        db=db,
        season_id=season_id,
        season=season,
        user_id=int(current_user.id)
    )


@router.delete("/{season_id}")
async def delete_season_route(
    season_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await delete_season(
        db=db,
        season_id=season_id,
        user_id=int(current_user.id)
    )