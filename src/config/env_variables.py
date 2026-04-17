"""

"""

from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    
    """
    # FastAPI configurations
    DEBUG: bool = True

    # User management engine configurations
    USER_MANAGEMENT_ENGINE_DATABASE_URL: str = "postgresql+asyncpg://postgres:password123@localhost:5432/user_management"
    USER_MANAGEMENT_ENGINE_ECHO: bool = False
    USER_MANAGEMENT_ENGINE_POOL_SIZE: int = 5
    USER_MANAGEMENT_ENGINE_MAX_OVERFLOW: int = 10
    USER_MANAGEMENT_ENGINE_POOL_TIMEOUT: int = 30
    USER_MANAGEMENT_ENGINE_POOL_RECYCLE: int = 1800
    USER_MANAGEMENT_ENGINE_FUTURE: bool = True

    # Username configuration
    USERNAME_MAX_LENGTH: int = 32

    # Password configuration
    PASSWORD_PEPPER: str


    model_config = ConfigDict(
        env_file=".env",
    )

environment_variables = Settings()
