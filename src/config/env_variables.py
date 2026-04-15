"""

"""

from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    
    """
    DEBUG: bool = True

    model_config = ConfigDict(
        env_file=".env",
    )

environment_variables = Settings()
