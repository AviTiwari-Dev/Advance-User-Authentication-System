"""

"""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from src.session_factories.user_management import user_management_session


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    
    """
    async with user_management_session as session:
        yield session
