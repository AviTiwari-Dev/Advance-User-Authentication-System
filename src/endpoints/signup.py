"""

"""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies.get_db_session import get_db_session
from src.models.data_validation.signup_base import SignupBase
from src.models.data_validation.user_profile_id import UserId
from src.operations.create_user import create_user
from src.routers.user_profile import user_profile_router


@user_profile_router.post(
    path="/signup",
    deprecated=False,
    description="User Sign Up",
    name="Signup",
    include_in_schema=True,
    response_model=UserId,
)
async def signup(user: SignupBase, db_session: Annotated[AsyncSession, Depends(get_db_session)]):
    """
    
    """
    user_id = await create_user(user.model_dump(), db_session)
    return {"user_id": user_id}
