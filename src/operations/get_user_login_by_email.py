"""

"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.data_storage.credential import Credential
from src.models.data_storage.email_address import EmailAddress
from src.models.data_storage.user import User


async def get_user_login_by_email(email_address: str, db_session: AsyncSession):
    """

    """
    statement = (
        select(User, Credential)
        .join(EmailAddress, EmailAddress.user_id == User.user_id)
        .join(Credential, Credential.user_id == User.user_id)
        .where(EmailAddress.email_address == email_address)
    )

    result = await db_session.execute(statement)
    return result.one_or_none()