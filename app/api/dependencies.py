from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
import uuid

from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy import select

from config import settings
from app.db.database import get_async_session
from db.models import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        session: AsyncSession = Depends(get_async_session)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось проверить учетные данные (токен недействителен)",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(token, settings.secret_key, settings.algorithm)
        user_id_str: str = payload.get("sub")

        if user_id_str is None:
            raise credentials_exception
        
        user_id = uuid.UUID(user_id_str)

    except jwt.InvalidTokenError:
        raise credentials_exception
    
    query = select(User).where(User.id == user_id)
    result = await session.execute(query)
    user = result.scalar_one_or_none()

    if user is None:
        raise credentials_exception
    
    return user
