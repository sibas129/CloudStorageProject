from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func, Sequence, UniqueConstraint, ForeignKeyConstraint

from database.orm._base_class import Base
from database.orm._annotations import (
    IntegerPrimaryKey,
    IntegerColumn,
    BoolColumn,
    TimestampWTColumn,
)


class M2M_FilesFolders(Base):
    __tablename__ = "m2m_files_folders"
    __table_args__ = (
        UniqueConstraint("folder_id", "file_id"),
        ForeignKeyConstraint(["folder_id"], ["folders.id"], ondelete="CASCADE"),
        ForeignKeyConstraint(["file_id"], ["files.id"], ondelete="CASCADE"),
    )
    id: Mapped[IntegerPrimaryKey] = mapped_column(Sequence("m2m_files_folders_id_seq"))
    file_id: Mapped[IntegerColumn] = mapped_column(index=True, nullable=False)
    folder_id: Mapped[IntegerColumn] = mapped_column(index=True, nullable=False)
    created_at: Mapped[TimestampWTColumn] = mapped_column(
        nullable=False, default=func.now()
    )
    updated_at: Mapped[TimestampWTColumn] = mapped_column(
        nullable=False, default=func.now(), onupdate=func.now()
    )
