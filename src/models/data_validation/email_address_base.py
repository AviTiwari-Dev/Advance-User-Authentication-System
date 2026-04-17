"""

"""

from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class EmailAddressBase(BaseModel):
    """
    
    """
    email_address: Annotated[
        EmailStr,
        Field(
            title="Email",
            description="Email",
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
