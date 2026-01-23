from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func, Sequence, UniqueConstraint, ForeignKeyConstraint

from database.orm._base_class import Base
from database.orm._annotations import (
    IntegerPrimaryKey,
    IntegerColumn,
    TimestampWTColumn,
)


class M2M_UsersOrganizations(Base):
    __tablename__ = "m2m_users_organizations"
    __table_args__ = (
        UniqueConstraint("user_id", "organization_id"),
        ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        ForeignKeyConstraint(["organization_id"], ["organizations.id"], ondelete="CASCADE"),
    )
    id: Mapped[IntegerPrimaryKey] = mapped_column(
        Sequence("m2m_users_organizations_id_seq")
    )
    user_id: Mapped[IntegerColumn] = mapped_column(index=True, nullable=False)
    organization_id: Mapped[IntegerColumn] = mapped_column(index=True, nullable=False)
    created_at: Mapped[TimestampWTColumn] = mapped_column(
        nullable=False, default=func.now()
    )
    updated_at: Mapped[TimestampWTColumn] = mapped_column(
        nullable=False, default=func.now(), onupdate=func.now()
    )
