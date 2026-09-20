from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from dependency import get_current_user
from models import User
from schema import QueryRequest, QueryResponse

from services.query import (
    get_farm_data_for_ai,
    get_farm_evidence
)

from services.ai import generate_ai_answer


router = APIRouter(
    prefix="/query",
    tags=["AI Query"]
)


@router.post("/", response_model=QueryResponse)
async def query(
    request: QueryRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # Get ONLY relevant farm records
    farm_data = await get_farm_data_for_ai(
        db=db,
        user_id=current_user.id,
        question=request.question
    )

    # Generate AI answer from relevant records
    answer = await generate_ai_answer(
        question=request.question,
        farm_data=farm_data
    )

    # Return the SAME relevant records as evidence
    evidence = await get_farm_evidence(
        db=db,
        user_id=current_user.id,
        question=request.question
    )

    return {
        "question": request.question,
        "answer": answer,
        "evidence": evidence
    }