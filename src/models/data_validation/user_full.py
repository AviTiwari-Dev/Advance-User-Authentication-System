"""

"""

from pydantic import ConfigDict

from src.models.data_validation.user_base import UserBase
from src.models.data_validation.user_id import UserId


class UserProfileFull(UserBase, UserId):
    """
    
    """
    
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
