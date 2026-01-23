from sqlalchemy import func, Sequence
from sqlalchemy.orm import Mapped, mapped_column

from database.orm._annotations import (
    IntegerPrimaryKey,
    TextColumn,
    TimestampWTColumn,
    IntegerColumn,
)
from database.orm._base_class import Base


class Files(Base):
    __tablename__ = "files"
    id: Mapped[IntegerPrimaryKey] = mapped_column(Sequence("files_id_seq"))
    name: Mapped[TextColumn] = mapped_column(nullable=False)
    path: Mapped[TextColumn] = mapped_column(nullable=False)
    created_at: Mapped[TimestampWTColumn] = mapped_column(
        nullable=True, default=func.now()
    )
    updated_at: Mapped[TimestampWTColumn] = mapped_column(
        nullable=True, default=func.now(), onupdate=func.now()
    )
    size: Mapped[IntegerColumn] = mapped_column(
        default=0, nullable=False,
    )
