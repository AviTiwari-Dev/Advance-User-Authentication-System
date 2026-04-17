"""

"""

from typing import Annotated

from pydantic import BaseModel, Field

from src.models.data_validation.password_base import PasswordBase


class LoginBase(PasswordBase):
    """
    
    """
    username: Annotated[
        str,
        Field(
            title="Username",
            description="Mandatory unique username",
            deprecated=False,
            min_length=2,
            max_length=32,
            pattern=r"^[a-z0-9_]+$",
            strict=True,
        )
    ]
