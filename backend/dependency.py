from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_db
from models import User
from jwt_handling import verify_access_token


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/users/token"
)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:

    payload = verify_access_token(token)

    user_id = payload.get("sub")

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token!"
        )

    try:
        user_id = int(user_id)

    except (TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token!"
        )

    result = await db.execute(
        select(User).where(User.id == user_id)
    )

    db_user = result.scalar_one_or_none()

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User Not Found!"
        )

    return db_user