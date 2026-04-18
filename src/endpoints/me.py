"""

"""

from typing import Annotated

from fastapi import Depends

from src.dependencies.get_current_user import get_current_user
from src.models.data_storage.user import User
from src.routers.user_profile import user_profile_router


@user_profile_router.get("/me")
async def get_me(
    current_user: Annotated[User, Depends(get_current_user)]
):
    return current_user