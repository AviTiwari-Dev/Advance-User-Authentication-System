"""

"""

from fastapi import APIRouter

user_profile_router = APIRouter(
    prefix="/user-profile",
    deprecated=False,
    include_in_schema=True,
    tags=["User Profile"],
)
