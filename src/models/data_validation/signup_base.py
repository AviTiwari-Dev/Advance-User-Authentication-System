"""

"""

from pydantic import ConfigDict

from src.models.data_validation.password_base import PasswordBase
from src.models.data_validation.user_profile_base import UserProfileBase


class SignupBase(UserProfileBase, PasswordBase):
    """
    
    """
    model_config = ConfigDict(
        extra="forbid",
        # json_schema_extra={
        #     "examples"=[

        #     ]
        # },
    )
