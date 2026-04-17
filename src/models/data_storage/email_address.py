"""

"""

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid7

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID as pgUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.bases.user_management import UserManagementBase
from src.enums.status import StatusEnum


class EmailAddress(UserManagementBase):
    __tablename__ = "email_addresses"
    __table_args__ = {"schema": "user_profile"}

    email_address_id: Mapped[UUID] = mapped_column(
        pgUUID(as_uuid=True), primary_key=True, default=uuid7
    )

    user_id: Mapped[UUID] = mapped_column(
        pgUUID(as_uuid=True),
        ForeignKey("user_profile.users.user_profile_id"),
        nullable=False
    )

    email_address: Mapped[str] = mapped_column(
        String, unique=True, index=True
    )

    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)

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

    user: Mapped["User"] = relationship(
        back_populates="email_addresses"
    )
