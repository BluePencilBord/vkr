from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.concurrency import run_in_threadpool
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import bcrypt

from app.db.database import get_async_session
from app.db.models import User
from app.schemas.users import CreateUser, CreateUserResponse
from app.schemas.token import TokenResponse

router = APIRouter()


def hash_password(password: str):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')


def verify_password(plain_password: str, hashed_password: str):
    password_bytes = plain_password.encode('utf-8')
    hash_bytes = hashed_password.encode('utf-8')

    return bcrypt.checkpw(password_bytes, hash_bytes)


@router.post("/register")
async def register_user(user_data: CreateUser, session: AsyncSession = Depends(get_async_session)):
    query = select(User).where(User.email == user_data.email)
    result = await session.execute(query)
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Пользователь с таким email уже существует"
        )
    
    hashed_password = hash_password(user_data.password)

    new_user = User(
        email = user_data.email,
        encrypted_password = hashed_password
    )

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return new_user


@router.post("/login")
async def login_user(user_data: CreateUser, session: AsyncSession = Depends(get_async_session)):
    query = select(User).where(User.email == user_data.email)
    result = await session.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=400, detail="Неверный email или пароль")
    
    is_password_correct = await run_in_threadpool(
        verify_password,
        user_data.password,
        user.encrypted_password
    )

    if not is_password_correct:
        raise HTTPException(status_code=400, detail="Неверный email или пароль")
    
    return TokenResponse(access_token=f"fake-jwt-token-for-{user.id}")
