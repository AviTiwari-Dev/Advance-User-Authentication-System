"""

"""

import asyncio
from typing import Annotated

from fastapi import Depends, HTTPException, Response, status
from sqlalchemy.exc import DBAPIError, OperationalError
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.env_variables import environment_variables
from src.dependencies.get_db_session import get_db_session
from src.models.data_validation.login_base import LoginBase
from src.operations.get_user_login_by_email import get_user_login_by_email
from src.operations.store_refresh_token import store_refresh_token
from src.routers.user_profile import user_profile_router
from src.utilities.password_hash import verify_hash
from src.utilities.tokens import create_access_token, create_refresh_token


@user_profile_router.post(
    path="/login",
    deprecated=False,
    description="User Login",
    name="Login",
    include_in_schema=True,
)
async def login(
    user: LoginBase,
    response: Response,
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
):
    """

    """
    max_retries = environment_variables.MAX_RETRIES
    base_delay = environment_variables.BASE_DELAY

    for attempt in range(1, max_retries + 1):
        try:
            user_login_record = await get_user_login_by_email(
                user.email_address,
                db_session,
            )

            if not user_login_record:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid email or password",
                )

            stored_user, credential = user_login_record

            if not verify_hash(user.password, credential.hashed_password):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid email or password",
                )

            access_token = create_access_token(str(stored_user.user_id))
            refresh_token = create_refresh_token(str(stored_user.user_id))

            await store_refresh_token(stored_user.user_id, refresh_token, db_session)
            await db_session.commit()

            response.set_cookie(
                key="refresh_token",
                value=refresh_token,
                httponly=True,
                secure=True,
                samesite="strict",
                max_age=7 * 24 * 60 * 60,
            )

            return {
                "access_token": access_token,
                "token_type": "bearer",
            }
        except HTTPException:
            await db_session.rollback()
            raise
        except (OperationalError, DBAPIError):
            await db_session.rollback()

            if attempt == max_retries:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Database temporarily unavailable. Please try again.",
                )

            delay = base_delay * (2 ** (attempt - 1))
            await asyncio.sleep(delay)
        except Exception:
            await db_session.rollback()
            raise