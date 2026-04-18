""" """

from fastapi import Depends, HTTPException, Request, Response
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.env_variables import environment_variables
from src.dependencies.get_db_session import get_db_session
from src.operations.get_refresh_token_by_jit import get_refresh_token_by_jti
from src.operations.invalidate_refresh_token import invalidate_refresh_token
from src.operations.store_refresh_token import store_refresh_token
from src.routers.user_profile import user_profile_router
from src.utilities.password_hash import verify_hash
from src.utilities.tokens import create_access_token, create_refresh_token


@user_profile_router.post("/refresh")
async def refresh_token(
    request: Request,
    response: Response,
    db_session: AsyncSession = Depends(get_db_session),
):
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        raise HTTPException(401, "Missing refresh token")

    try:
        payload = jwt.decode(
            refresh_token,
            environment_variables.SECRET_KEY,
            algorithms=[environment_variables.ALGORITHM],
        )
    except JWTError:
        raise HTTPException(401, "Invalid refresh token")

    if payload.get("type") != "refresh":
        raise HTTPException(401, "Invalid token type")

    user_id = payload.get("sub")
    jti = payload.get("jti")

    # 🔐 Get stored token
    stored_token = await get_refresh_token_by_jti(jti, db_session)

    if not stored_token:
        raise HTTPException(401, "Token not found")

    # 🔐 Verify hash
    if not verify_hash(refresh_token, stored_token.hashed_refresh_token):
        raise HTTPException(401, "Token mismatch")

    # 🔥 ROTATE TOKEN
    await invalidate_refresh_token(stored_token, db_session)

    new_access_token = create_access_token(user_id)
    new_refresh_token = create_refresh_token(user_id)

    await store_refresh_token(user_id, new_refresh_token, db_session)

    await db_session.commit()

    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=7 * 24 * 60 * 60,
    )

    return {
        "access_token": new_access_token,
        "token_type": "bearer",
    }
