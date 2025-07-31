from fastapi import APIRouter
from .user import user_router
from .card import card_route
from .auth import auth_router
from .travel import travel_route
router = APIRouter()
router.include_router(user_router)
router.include_router(card_route)
router.include_router(auth_router)
router.include_router(travel_route)
