"""

"""

from typing import Annotated

from fastapi import Depends, HTTPException, Request, Response, status
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.env_variables import environment_variables
from src.dependencies.get_current_user import get_current_user
from src.dependencies.get_db_session import get_db_session
from src.models.data_storage.user import User
from src.operations.get_stored_refresh_token import get_stored_refresh_token
from src.routers.user_profile import user_profile_router


@user_profile_router.post(
	path="/logout",
	deprecated=False,
	description="User Logout",
	name="Logout",
	include_in_schema=True,
	status_code=status.HTTP_204_NO_CONTENT,
)
async def logout(
	request: Request,
	response: Response,
	current_user: Annotated[User, Depends(get_current_user)],
	db_session: Annotated[AsyncSession, Depends(get_db_session)],
):
	"""

	"""
	refresh_token = request.cookies.get("refresh_token")

	if not refresh_token:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="User is not currently logged in",
		)

	try:
		payload = jwt.decode(
			refresh_token,
			environment_variables.SECRET_KEY,
			algorithms=[environment_variables.ALGORITHM],
		)
	except JWTError:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Invalid refresh token",
		)

	if payload.get("type") != "refresh":
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Invalid token type",
		)

	if payload.get("sub") != str(current_user.user_id):
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Refresh token does not belong to the current user",
		)

	stored_token = await get_stored_refresh_token(
		current_user.user_id,
		refresh_token,
		db_session,
	)

	if not stored_token:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="User is not currently logged in",
		)

	await db_session.delete(stored_token)
	await db_session.commit()

	response.delete_cookie(
		key="refresh_token",
		httponly=True,
		secure=True,
		samesite="strict",
	)

	return None
