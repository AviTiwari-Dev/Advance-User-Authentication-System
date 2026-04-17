"""

"""

from sqlalchemy.ext.asyncio import create_async_engine

from ..config.env_variables import environment_variables

user_management_engine = create_async_engine(
    url=environment_variables.USER_MANAGEMENT_ENGINE_DATABASE_URL,
    echo=environment_variables.USER_MANAGEMENT_ENGINE_ECHO,
    pool_size=environment_variables.USER_MANAGEMENT_ENGINE_POOL_SIZE,
    max_overflow=environment_variables.USER_MANAGEMENT_ENGINE_MAX_OVERFLOW,
    pool_timeout=environment_variables.USER_MANAGEMENT_ENGINE_POOL_TIMEOUT,
    pool_recycle=environment_variables.USER_MANAGEMENT_ENGINE_POOL_RECYCLE,
    future=environment_variables.USER_MANAGEMENT_ENGINE_FUTURE,
    connect_args={"server_settings": {"jit": "off"}},
)
