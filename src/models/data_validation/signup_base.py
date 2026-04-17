"""

"""

from datetime import date
from typing import Annotated

from pydantic import ConfigDict, Field

from src.enums.gender import GenderEnum
from src.models.data_validation.email_address_base import EmailAddressBase
from src.models.data_validation.full_name_base import FullNameBase
from src.models.data_validation.login_base import LoginBase
from src.models.data_validation.user_profile_base import UserProfileBase


class SignupBase(UserProfileBase, LoginBase):
    """
    
    """
    model_config = ConfigDict(
        extra="forbid",
        # json_schema_extra={
        #     "examples"=[

        #     ]
        # },
    )
