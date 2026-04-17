import re
import secrets
import string

from src.config.env_variables import environment_variables

MAX_LENGTH = environment_variables.USERNAME_MAX_LENGTH

def normalize_name(name: str) -> str:
    name = name.lower()
    name = re.sub(r'[^a-z]', '', name)  # keep only letters
    return name


def generate_username(first_name: str) -> str:
    base = normalize_name(first_name)

    # Ensure base is not empty
    if not base:
        base = "user"

    # Reserve space for "_" + random part
    remaining_length = MAX_LENGTH - len(base) - 1

    # If name too long, trim it
    if remaining_length <= 0:
        base = base[:MAX_LENGTH - 1]
        remaining_length = 1

    random_part = ''.join(
        secrets.choice(string.ascii_lowercase + string.digits)
        for _ in range(remaining_length)
    )

    return f"{base}_{random_part}"
