"""

"""

from datetime import datetime, timedelta, timezone
from uuid import uuid7

from jose import jwt

from src.config.env_variables import environment_variables


def create_access_token(user_id: str):
    payload = {
        "sub": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=15),
        "type": "access"
    }
    return jwt.encode(payload, environment_variables.SECRET_KEY, algorithm=environment_variables.ALGORITHM)


def create_refresh_token(user_id: str):
    payload = {
        "sub": user_id,
        "jti": str(uuid7()),  # unique token id
        "exp": datetime.now(timezone.utc) + timedelta(days=7),
        "type": "refresh"
    }
    return jwt.encode(payload, environment_variables.SECRET_KEY, algorithm=environment_variables.ALGORITHM)
