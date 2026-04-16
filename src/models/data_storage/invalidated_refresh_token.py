"""

"""

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid7

from sqlalchemy import DateTime, Enum, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID as pgUUID
from sqlalchemy.orm import Mapped, mapped_column

from bases.user_management import UserManagementBase
from enums.status import StatusEnum


class InvalidatedRefreshToken(UserManagementBase):
    __tablename__ = "invalidated_refresh_tokens"
    __table_args__ = {"schema": "auth"}

    invalidated_refresh_token_id: Mapped[UUID] = mapped_column(
        pgUUID(as_uuid=True),
        primary_key=True,
        default=uuid7
    )

    user_id: Mapped[UUID] = mapped_column(
        pgUUID(as_uuid=True),
        ForeignKey("user_profile.users.user_profile_id"),
        nullable=False,
        index=True,
    )

    hashed_refresh_token: Mapped[str] = mapped_column(
        String,
        nullable=False,
        index=True
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    status: Mapped[StatusEnum] = mapped_column(
        Enum(StatusEnum),
        default=StatusEnum.active
    )
