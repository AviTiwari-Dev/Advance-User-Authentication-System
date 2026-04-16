"""

"""

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from engines.user_management import user_management_engine

user_management_session = async_sessionmaker(
    bind=user_management_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    auto_flush=True,
)
