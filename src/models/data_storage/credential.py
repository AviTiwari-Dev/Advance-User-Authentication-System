"""

"""

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid7

from sqlalchemy import DateTime, Enum, String, func
from sqlalchemy.dialects.postgresql import UUID as pgUUID
from sqlalchemy.orm import Mapped, mapped_column

from src.bases.user_management import UserManagementBase
from src.enums.status import StatusEnum


class Credential(UserManagementBase):
    __tablename__ = "credentials"
    __table_args__ = {"schema": "auth"}

    credential_id: Mapped[UUID] = mapped_column(
        pgUUID(as_uuid=True),
        primary_key=True,
        default=uuid7
    )

    user_id: Mapped[UUID] = mapped_column(
        pgUUID(as_uuid=True),
        nullable=False,
        unique=True,
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
    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    status: Mapped[StatusEnum] = mapped_column(
        Enum(StatusEnum),
        default=StatusEnum.active
    )
