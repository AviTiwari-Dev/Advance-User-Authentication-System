"""

"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    
    """
    # FastAPI configurations
    DEBUG: bool = True

    # User management engine configurations
    USER_MANAGEMENT_ENGINE_DATABASE_URL: str
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
    
    # Exponential retries configurations
    MAX_RETRIES: int = 3
    BASE_DELAY: float = 0.1

    # Token configurations
    SECRET_KEY: str
    ALGORITHM: str = "HS256"

    model_config = SettingsConfigDict(
        env_file=".env",
    )

environment_variables = Settings()
