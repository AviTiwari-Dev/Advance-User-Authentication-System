"""

"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.data_storage.refresh_token import RefreshToken


# Invalidate token
async def invalidate_refresh_token(
    token: RefreshToken, db_session: AsyncSession
):
    token.is_revoked = True
