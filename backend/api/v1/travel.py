from fastapi import Query

from fastapi import APIRouter
from fastapi.params import Depends
from backend.dependencies import is_user
from backend.models import AsyncSession, get_session
from typing import Annotated
from backend.schemas.auth import UserForToken
from backend.service.auth import AuthService
travel_route = APIRouter(prefix="/travel", tags=["travel"])

@travel_route.post("/")
async def create_travel(user: Annotated[UserForToken, Depends(is_user)], session: Annotated[AsyncSession, Depends(get_session)]) -> UserForToken:
    return user