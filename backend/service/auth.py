from datetime import timedelta, datetime
import os
from os import access
from passlib.context import CryptContext
import jwt
from fastapi import Header, Request, HTTPException
from sqlalchemy.util import deprecated

from backend.schemas.user import UserAuthentication, UserRead
from backend.schemas.auth import UserForToken
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
    @staticmethod
    def create_access_token(data: UserForToken, expires_delta: timedelta = timedelta(minutes=5)):
        try:
            to_encode = data.model_dump()
            expire = datetime.utcnow() + expires_delta
            to_encode.update({"expire": int(expire.timestamp())})
            print(os.getenv('ALGORITHM', 'HS256'))
            access_token = jwt.encode(to_encode, os.getenv('SECRET_KEY', 'mysecretkey'), algorithm=os.getenv('ALGORITHM', 'HS256'))
            return access_token
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

