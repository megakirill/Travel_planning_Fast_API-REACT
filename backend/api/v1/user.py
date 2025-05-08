from fastapi import APIRouter

user_router = APIRouter(
    prefix="/user",
    tags=["user"]
)

@user_router.get("/{id}")
async def get_user(id: int):
    return {"id": id}
