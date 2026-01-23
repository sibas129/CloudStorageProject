from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func, Sequence, UniqueConstraint, ForeignKeyConstraint

from database.orm._base_class import Base
from database.orm._annotations import (
    IntegerPrimaryKey,
    IntegerColumn,
    BoolColumn,
    TimestampWTColumn,
)


class M2M_FoldersFolders(Base):
    __tablename__ = "m2m_folders_folders"
    __table_args__ = (
        UniqueConstraint("child_folder_id"),
        ForeignKeyConstraint(["parent_folder_id"], ["folders.id"], ondelete="CASCADE"),
        ForeignKeyConstraint(["child_folder_id"], ["folders.id"], ondelete="CASCADE"),
    )
    id: Mapped[IntegerPrimaryKey] = mapped_column(
        Sequence("m2m_folders_folders_id_seq")
    )
    parent_folder_id: Mapped[IntegerColumn] = mapped_column(index=True, nullable=False)
    child_folder_id: Mapped[IntegerColumn] = mapped_column(index=True, nullable=False)
    created_at: Mapped[TimestampWTColumn] = mapped_column(
        nullable=False, default=func.now()
    )
    updated_at: Mapped[TimestampWTColumn] = mapped_column(
        nullable=False, default=func.now(), onupdate=func.now()
    )
