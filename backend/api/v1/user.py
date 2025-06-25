from typing import Annotated, Union, Optional, Any, Coroutine
from fastapi import APIRouter, Response, HTTPException, Query, Depends, Path
from backend.repo import UserRepository
from backend.schemas.user import *
from backend.models import AsyncSession, get_session
from backend.service.user import UserService

user_router = APIRouter(
    prefix="/user",
    tags=["user"]
)

async def get_user_from_service(session: Annotated[AsyncSession, Depends(get_session)], user_id: int = Path(...)) -> User:
    a = await UserRepository.get_user(session, user_id)
    if a is None:
        raise HTTPException(status_code=404, detail="User not found")
    return a


@user_router.post("/create", responses={
    200: {'description': 'success'},
    404: {'description': 'This email is already in use'},
    500: {'description': 'The server error'}})
async def create_user(user: UserCreate) -> UserRead:
    try:
        result = await UserService.create_user(user)
        if result is None:
            raise HTTPException(status_code=404, detail="User not found")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@user_router.delete("/{id}", responses={
    200: {'description': 'success'}
})
async def delete_user(id: int):
    try:
        a = await UserService.delete_user(id)
        if a:
            return {'result': 'done'}
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@user_router.get("/")
async def get_user_by_id(id: Annotated[Optional[int], Query()] = None, email :Annotated[Optional[str], Query()] = None) -> UserRead:
    try:
        if id is not None:
            result = await UserService.get_user_by_id(id)
            if result is None:
                raise HTTPException(status_code=404, detail="User not found")
        elif email is not None:
            result = await UserService.get_user_by_email(email)
            if result is None:
                raise HTTPException(status_code=404, detail="User not found")
        else:
            raise HTTPException(status_code=404, detail="No id or email provided")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@user_router.patch("/{user_id}", responses={})
async def update_user(user_id: int,
    session: Annotated[AsyncSession, Depends(get_session)],
    user: Annotated[User, Depends(get_user_from_service)],
    user_new: UserUpdate
) -> UserRead:
    try:
        a = await UserService.update_user(session, user, user_new)
        return a.model_dump()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))







