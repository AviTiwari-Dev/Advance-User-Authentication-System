"""

"""

from typing import Annotated

from pydantic import BaseModel, Field


class PasswordBase(BaseModel):
    """
    
    """
    password: Annotated[
        str,
        Field(
            title="Password",
            description="Mandatory password",
            deprecated=False,
            min_length=8,
            max_length=32,
            pattern=r"^[a-z0-9-+@#]+$",
            strict=True,
        )
    ]
