"""

"""

from datetime import datetime, timezone
from uuid import UUID

from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.env_variables import environment_variables
from src.models.data_storage.invalidated_refresh_token import InvalidatedRefreshToken
from src.utilities.password_hash import hash_string


async def store_refresh_token(
    user_id: UUID,
    refresh_token: str,
    db_session: AsyncSession
):
    """
    
    """
    # Hash token (never store raw token)
    hashed_token = hash_string(refresh_token)

    # Decode token to get expiry
    payload = jwt.decode(
        refresh_token,
        environment_variables.SECRET_KEY,
        algorithms=[environment_variables.ALGORITHM],
    )

    expires_at = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)

    # Create DB object
    token_data = InvalidatedRefreshToken(
        user_id=user_id,
        hashed_refresh_token=hashed_token,
        expires_at=expires_at,
        status="active",
    )

    # Add to session (NO commit)
    db_session.add(token_data)

    # Flush (optional but recommended to catch issues early)
    await db_session.flush()
