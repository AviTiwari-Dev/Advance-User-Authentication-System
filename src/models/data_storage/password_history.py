"""

"""

from datetime import datetime
from uuid import UUID, uuid7

from sqlalchemy import DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID as pgUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bases.user_management import UserManagementBase


class PasswordHistory(UserManagementBase):
    __tablename__ = "password_histories"
    __table_args__ = {"schema": "auth"}

    password_history_id: Mapped[UUID] = mapped_column(
        pgUUID(as_uuid=True),
        primary_key=True,
        default=uuid7
    )

    user_id: Mapped[UUID] = mapped_column(
        pgUUID(as_uuid=True),
        nullable=False,
        index=True
    )

    hashed_password: Mapped[str] = mapped_column(String, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
