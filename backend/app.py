from fastapi import FastAPI, Header, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.testing.provision import drop_db

from api import api_router
from backend.models import init_db
from schemas.user import UserAuthentication
from typing import Annotated

app = FastAPI()

@app.get("/")
async def root():
    await init_db()
    return {"message": "Hello World"}

@app.post("/login")
async def login():
    await init_db()

app.include_router(api_router, prefix="/api")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")