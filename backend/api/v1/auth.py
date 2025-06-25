from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from backend.models import get_session
from backend.schemas import UserWithToken, UserLogin
from fastapi import Cookie, HTTPException, APIRouter, Depends, Response
from fastapi.responses import JSONResponse
import jwt
from jwt import PyJWTError
import os
from backend.service.user import UserService
from backend.service.auth import AuthService
auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.post("/login")
async def login(user: UserLogin, session: AsyncSession = Depends(get_session)):
    try:
        user_data = await UserService.login_user(session, user)
        if not user_data:
            raise HTTPException(status_code=404, detail="User not found")
        print('a')
        access_token = AuthService.create_access_token(user_data)
        print('b')
        print('c')
        return JSONResponse(
            status_code=200,
            content={
                "name": user_data.name,
                "email": user_data.email,
            },
            headers={"Authorization": f"Bearer {access_token}"}
        )
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))










async def get_access_token(token: Annotated[str, Cookie()]):
    try:
        token = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=[os.getenv('ALGORITHM')])
        return token['sub']
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")




