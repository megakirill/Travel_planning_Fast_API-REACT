from typing import Annotated

from fastapi import HTTPException, Depends

from backend.schemas import UserForToken
from backend.service.auth import AuthService
auth = AuthService()


async def is_user(data: Annotated[UserForToken, Depends(auth.verify_access_token)]) -> UserForToken:
    if data.role == 'user':
        return data
    else:
        raise HTTPException(status_code=401, detail="No rights")