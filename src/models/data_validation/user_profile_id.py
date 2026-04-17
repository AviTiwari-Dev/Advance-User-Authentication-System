"""

"""

from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class UserId(BaseModel):
    """
    
    """
    user_id: Annotated[
        UUID,
        Field(
            title="User ID",
            description="User id along with other feilds of user profile",
            deprecated=False,
            strict=True,
        )
    ]

    model_config = ConfigDict(
        str_to_lower=True,
        extra="forbid",
        cache_strings=True,
        # use_enum_values=False,
        validate_default=True,
        validate_assignment=True,
        # revalidate_instances=True,
        # json_schema_extra={
        #     "examples"=[

        #     ]
        # },
    )
