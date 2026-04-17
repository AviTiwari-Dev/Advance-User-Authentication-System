"""

"""

from datetime import date, datetime
from typing import List, Optional
from uuid import UUID, uuid7

from sqlalchemy import Date, DateTime, Enum, String, func
from sqlalchemy.dialects.postgresql import UUID as pgUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.bases.user_management import UserManagementBase
from src.enums.gender import GenderEnum
from src.enums.status import StatusEnum


class User(UserManagementBase):
    __tablename__ = "users"
    __table_args__ = {"schema": "user_profile"}

    user_id: Mapped[UUID] = mapped_column(
        pgUUID(as_uuid=True),
        primary_key=True,
        default=uuid7
    )

    username: Mapped[str] = mapped_column(String(32), unique=True, index=True)

    first_name: Mapped[str] = mapped_column(String(25))
    middle_name: Mapped[Optional[str]] = mapped_column(String(25), nullable=True)
    last_name: Mapped[str] = mapped_column(String(25))

    date_of_birth: Mapped[date] = mapped_column(Date)
    gender: Mapped[GenderEnum] = mapped_column(Enum(GenderEnum))

    username_update_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
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

    email_addresses: Mapped[List["EmailAddress"]] = relationship(
        back_populates="user_profile",
        cascade="all, delete-orphan"
    )
