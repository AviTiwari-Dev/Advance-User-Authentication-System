"""

"""

import asyncio
from typing import Annotated

from fastapi import Depends, HTTPException, Response, status
from sqlalchemy.exc import DBAPIError, IntegrityError, OperationalError
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.env_variables import environment_variables
from src.dependencies.get_db_session import get_db_session
from src.models.data_validation.signup_base import SignupBase
from src.operations.create_user import create_user
from src.operations.store_refresh_token import store_refresh_token
from src.routers.user_profile import user_profile_router
from src.utilities.tokens import create_access_token, create_refresh_token


@user_profile_router.post(
    path="/signup",
    deprecated=False,
    description="User Sign Up",
    name="Signup",
    include_in_schema=True,
    # response_model=UserId,
)
async def signup(
    user: SignupBase,
    response: Response,
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
):
    """
    
    """
    MAX_RETRIES = environment_variables.MAX_RETRIES
    BASE_DELAY = environment_variables.BASE_DELAY

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            # Create user
            user_id = await create_user(user.model_dump(), db_session)

            # Create tokens
            access_token = create_access_token(str(user_id))
            refresh_token = create_refresh_token(str(user_id))

            # Store refresh token
            await store_refresh_token(user_id, refresh_token, db_session)

            # Commit transactions
            await db_session.commit()
            
            # Set refresh token in cookie
            response.set_cookie(
                key="refresh_token",
                value=refresh_token,
                httponly=True,
                secure=True,
                samesite="strict",
                max_age=7*24*60*60
            )

            return {
                "access_token": access_token,
                "token_type": "bearer",
            }
        except IntegrityError as e:
            await db_session.rollback()

            error_msg = str(e.orig).lower()

            if "email" in error_msg:
                raise HTTPException(400, "Email already exists")

            raise
        except (OperationalError, DBAPIError):
            await db_session.rollback()
            if attempt == MAX_RETRIES:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Database temporarily unavailable. Please try again.",
                )

            delay = BASE_DELAY * (2 ** (attempt - 1))
            await asyncio.sleep(delay)

        except Exception:
            await db_session.rollback()
            raise
