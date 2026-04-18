"""

"""

from datetime import datetime, timezone
from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies.get_current_user import get_current_user
from src.dependencies.get_db_session import get_db_session
from src.models.data_storage.user import User
from src.routers.user_profile import user_profile_router


@user_profile_router.patch(
    path="/username",
    description="Change username",
)
async def change_username(
    new_username: str,
    current_user: Annotated[User, Depends(get_current_user)],
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
):
    """
    Change username for logged-in user
    """

    # Check if username already exists
    result = await db_session.execute(
        select(User).where(User.username == new_username)
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken",
        )

    try:
        # Update username
        current_user.username = new_username
        current_user.username_update_at = datetime.now(timezone.utc)

        # Commit
        await db_session.commit()

        return {
            "message": "Username updated successfully",
            "username": new_username,
        }

    except IntegrityError:
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken",
        )