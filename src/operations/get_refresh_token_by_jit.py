"""

"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.data_storage.refresh_token import RefreshToken


# Get token by JTI
async def get_refresh_token_by_jti(
    jti: str, db_session: AsyncSession
) -> RefreshToken | None:
    result = await db_session.execute(
        select(RefreshToken).where(RefreshToken.jti == jti)
    )
    return result.scalar_one_or_none()
