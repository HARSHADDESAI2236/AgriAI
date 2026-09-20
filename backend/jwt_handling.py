from jose import jwt, JWTError
from fastapi import HTTPException, status

from datetime import datetime, timedelta, timezone


SECRET_KEY = "AGRIAI2026"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(data: dict):

    to_encode = data.copy()

    expire_time = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({
        "exp": expire_time
    })

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt


def verify_access_token(token: str):

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or Expired Token!"
        )