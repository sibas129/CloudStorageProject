from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func, Sequence, UniqueConstraint, ForeignKeyConstraint

from database.orm._base_class import Base
from database.orm._annotations import (
    IntegerPrimaryKey,
    IntegerColumn,
    BoolColumn,
    TimestampWTColumn,
)


class M2M_OrganizationsFolders(Base):
    __tablename__ = "m2m_organizations_folders"
    __table_args__ = (
        UniqueConstraint("organization_id", "folder_id"),
        ForeignKeyConstraint(["organization_id"], ["organizations.id"], ondelete="CASCADE"),
        ForeignKeyConstraint(["folder_id"], ["folders.id"], ondelete="CASCADE"),
    )
    id: Mapped[IntegerPrimaryKey] = mapped_column(
        Sequence("m2m_organizations_folders_id_seq")
    )
    organization_id: Mapped[IntegerColumn] = mapped_column(index=True, nullable=False)
    folder_id: Mapped[IntegerColumn] = mapped_column(index=True, nullable=False)
    is_root: Mapped[BoolColumn] = mapped_column(
        index=True, nullable=False, default=False
    )
    created_at: Mapped[TimestampWTColumn] = mapped_column(
        nullable=False, default=func.now()
    )
    updated_at: Mapped[TimestampWTColumn] = mapped_column(
        nullable=False, default=func.now(), onupdate=func.now()
    )
