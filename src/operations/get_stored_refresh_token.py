"""

"""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.data_storage.invalidated_refresh_token import InvalidatedRefreshToken
from src.utilities.password_hash import verify_hash


async def get_stored_refresh_token(
    user_id: UUID,
    refresh_token: str,
    db_session: AsyncSession,
):
    """

    """
    statement = select(InvalidatedRefreshToken).where(
        InvalidatedRefreshToken.user_id == user_id,
    )
    result = await db_session.execute(statement)
    stored_tokens = result.scalars().all()

    for stored_token in stored_tokens:
        if verify_hash(refresh_token, stored_token.hashed_refresh_token):
            return stored_token

    return None