"""

"""


from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.data_storage.credential import Credential
from src.models.data_storage.user import User
from src.utilities.password_hash import hash_password
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
    
    try:
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

                # Create credentials
                credential_data = Credential(
                    user_id=user_id,
                    hashed_password=hash_password(user["password"]),
                )
                db_session.add(credential_data)

                # Commit transaction
                await db_session.commit()

                await db_session.refresh(user_data)

                return user_id
            
            except IntegrityError:
                await db_session.rollback()
                continue
            
        raise ValueError("Failed to generate unique username after retries")
        
    except Exception:
        await db_session.rollback()
        raise
