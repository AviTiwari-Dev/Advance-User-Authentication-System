"""

"""


from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.data_storage.credential import Credential
from src.models.data_storage.email_address import EmailAddress
from src.models.data_storage.user import User
from src.utilities.password_hash import hash_string
from src.utilities.username import generate_username


async def create_user(user, db_session: AsyncSession):
    """
    user parameter is dict of
        password            Mandatory
        first_name          Mandatory
        middle_name         Optional if no last_name
        last_name           Mandatory if middle_name provided
        date_of_birth       Mandatory
        gender              Mandatory
    """

    if user.get("middle_name") and not user.get("last_name"):
        raise ValueError("Last name is required when middle name is provided")
    
    for _ in range(5):
        # Generate unique username of 32 characters
        username = generate_username(user["first_name"])

        # Add user to db
        try:
            user_data = User(
                username=username,
                first_name=user["first_name"],
                middle_name=user.get("middle_name"),
                last_name=user.get("last_name"),
                date_of_birth=user["date_of_birth"],
                gender=user["gender"],
            )
            db_session.add(user_data)
            await db_session.flush()
            user_id = user_data.user_id

            # Create email
            email_data = EmailAddress(
                user_id=user_id,
                email_address=user["email_address"],
            )
            db_session.add(email_data)

            # Create credentials
            credential_data = Credential(
                user_id=user_id,
                hashed_password=hash_string(user["password"]),
            )
            db_session.add(credential_data)
            await db_session.flush()

            return user_id
        
        except IntegrityError as e:
            # await db_session.rollback()
            raise e
        
    raise ValueError("Failed to generate unique username after retries")
