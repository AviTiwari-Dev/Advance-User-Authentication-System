"""

"""

from datetime import date
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, model_validator


class UserProfileBase(BaseModel):
    """
    
    """
    first_name: Annotated[
        str,
        Field(
            title="First Name",
            description="Mandatory first name.",
            deprecated=False,
            min_length=2,
            max_length=25,
            pattern=r"^[a-zA-Z]+$",
            strict=True,
        )
    ]
    middle_name: Annotated[
        None | str,
        Field(
            title="Middle Name",
            description="Optional middle name.",
            deprecated=False,
            min_length=2,
            max_length=25,
            pattern=r"^[a-zA-Z]+$",
            strict=True,
        )
    ] = None
    last_name: Annotated[
        None | str,
        Field(
            title="Last Name",
            description="Optional middle name (mandatory when middle_name is provided).",
            deprecated=False,
            min_length=2,
            max_length=25,
            pattern=r"^[a-zA-Z]+$",
            strict=True,
        )
    ] = None
    date_of_birth: Annotated[
        date,
        Field(
            title="Date of Birth",
            description="Date of birth",
            deprecated=False,
            strict=True,
        )
    ]

    @model_validator(mode="after")
    def validate_middle_name_and_last_name(self):
        """
        
        """
        if self.middle_name and not self.last_name:
            raise ValueError("Last name is required when middle name is provided")
        return self
    

    model_config = ConfigDict(
        str_to_lower=True,
        extra="forbid",
        cache_strings=True,
        use_enum_values=False,
        validate_default=True,
        validate_assignment=True,
        revalidate_instances=True,
        # json_schema_extra={
        #     "examples"=[

        #     ]
        # },
    )
