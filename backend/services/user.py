from models import User
from schema import CreateUser,LoginUser,UpdateUser
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from hash import hash_pwd,verify_pwd
from jwt_handling import create_access_token
from fastapi import HTTPException,status


async def create_user(db:AsyncSession,user:CreateUser):

    result=await db.execute(
        select(User).where(User.email==user.email)
    )

    email=result.scalar_one_or_none()

    if email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email Already Exists!"
        )


    new_user=User(
        username=user.username,
        email=user.email,
        password=hash_pwd(user.password)
    )

    db.add(new_user)

    await db.commit()

    await db.refresh(new_user)

    return new_user



async def verify_user(
    db: AsyncSession,
    email: str,
    password: str
):
    result = await db.execute(
        select(User).where(User.email == email)
    )

    db_user = result.scalars().first()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User Not Found!"
        )

    if not verify_pwd(
        password,
        db_user.password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Email or Password!"
        )

    access_token = create_access_token({
        "sub": str(db_user.id),
        
    })

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }




async def update_user(
    db: AsyncSession,
    user: UpdateUser,
    user_id: int,
):
    result = await db.execute(select(User).where(User.id == user_id))
    db_user = result.scalars().first()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User Not Found!",
        )

    if user.email is not None and user.email != db_user.email:
        email_result = await db.execute(select(User).where(User.email == user.email))
        if email_result.scalars().first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email Already Exists!",
            )
        db_user.email = user.email

    if user.username is not None:
        db_user.username = user.username

    if user.password is not None:
        db_user.password = hash_pwd(user.password)

    await db.commit()
    await db.refresh(db_user)
    return db_user


async def delete_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).where(User.id == user_id))
    db_user = result.scalars().first()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User Not Found!",
        )

    farmer_result = await db.execute(select(User).where(User.id == user_id))
    if farmer_result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Delete the Farmer profile before deleting the User!",
        )

    await db.delete(db_user)
    await db.commit()
    return {"detail": "User deleted successfully!"}


