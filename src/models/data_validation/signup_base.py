"""

"""

from pydantic import ConfigDict

from src.models.data_validation.password_base import PasswordBase
from src.models.data_validation.user_base import UserBase


class SignupBase(UserBase, PasswordBase):
    """
    
    """
    model_config = ConfigDict(
        extra="forbid",
        # json_schema_extra={
        #     "examples"=[

        #     ]
        # },
    )
