from datetime import timedelta, datetime
import os
from os import access

from fastapi.params import Depends
from passlib.context import CryptContext
import jwt
from fastapi import Header, Request, HTTPException
from typing import Annotated
from sqlalchemy.util import deprecated
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from backend.schemas.user import UserAuthentication, UserRead
from backend.schemas.auth import UserForToken

security_token = HTTPBearer()

class Crypto:
    __context = CryptContext(
        schemes=["bcrypt"],
        deprecated="auto",
        bcrypt__rounds=12,
    )

    @staticmethod
    def create_hash(password: str)-> str:
        return Crypto.__context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return Crypto.__context.verify(plain_password, hashed_password)


class AuthService:
    SECRET_KEY = os.getenv('SECRET_KEY', 'mysecretkey')
    ALGORITHM = os.getenv('ALGORITHM', 'HS256')
    @classmethod
    def create_access_token(cls, data: UserForToken, expires_delta: timedelta = timedelta(minutes=5)):
        '''создает access token'''
        try:
            to_encode = data.model_dump()
            expire = datetime.utcnow() + expires_delta
            to_encode.update({"exp": int(expire.timestamp())})
            print(cls.SECRET_KEY, cls.ALGORITHM)
            access_token = jwt.encode(to_encode, cls.SECRET_KEY, algorithm=cls.ALGORITHM)
            print(access_token)
            return access_token
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))

    @classmethod
    def verify_access_token(cls, token: Annotated[HTTPAuthorizationCredentials, Depends(security_token)]) -> UserForToken:
        """проверяет access_token"""
        try:
            print(cls.SECRET_KEY, cls.ALGORITHM)
            print(token.credentials)
            data = jwt.decode(token.credentials, cls.SECRET_KEY, algorithms=[cls.ALGORITHM])
            user = UserForToken(**data)
            return user
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=404, detail="Expired token")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=404, detail="Invalid token")
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))

    @staticmethod
    def create_hash_password(password: str) -> str:
        con = Crypto.create_hash(password)
        return con
    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        is_verified = Crypto.verify_password(password, hashed_password)
        return is_verified