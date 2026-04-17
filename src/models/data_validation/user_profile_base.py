"""

"""

from datetime import date
from typing import Annotated

from pydantic import ConfigDict, Field

from src.enums.gender import GenderEnum
from src.models.data_validation.email_address_base import EmailAddressBase
from src.models.data_validation.full_name_base import FullNameBase
from src.models.data_validation.login_base import LoginBase


class UserProfileBase(FullNameBase, EmailAddressBase):
    """
    
    """
    date_of_birth: Annotated[
        date,
        Field(
            title="Date of Birth",
            description="Date of birth",
            deprecated=False,
            strict=True,
        )
    ]
    gender: Annotated[
        GenderEnum,
        Field(
            title="Gender",
            description="Gender",
            deprecated=False,
            strict=True,
        )
    ]
    model_config = ConfigDict(
        extra="forbid",
        # json_schema_extra={
        #     "examples"=[

        #     ]
        # },
    )
