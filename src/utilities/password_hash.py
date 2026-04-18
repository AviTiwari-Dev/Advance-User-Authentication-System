"""

"""

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from src.config.env_variables import environment_variables

# 🔐 Config (tune if needed)
ph = PasswordHasher(
    time_cost=3,       # iterations
    memory_cost=65536, # KB (64 MB)
    parallelism=2
)

PEPPER = environment_variables.PASSWORD_PEPPER


def hash_string(string: str) -> str:
    """
    Hash password using Argon2 + pepper
    """
    password_peppered = string + PEPPER
    return ph.hash(password_peppered)


def verify_hash(password: str, hashed_password: str) -> bool:
    """
    Verify password safely
    """
    try:
        password_peppered = password + PEPPER
        return ph.verify(hashed_password, password_peppered)
    except VerifyMismatchError:
        return False
