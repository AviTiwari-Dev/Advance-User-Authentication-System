"""

"""

from pydantic import BaseModel, Field


class ChangeUserName(BaseModel):
    username: str = Field(min_length=3, max_length=32, pattern=r"^[a-z0-9_]+$")