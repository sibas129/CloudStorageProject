from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func, Sequence, UniqueConstraint

from database.orm._base_class import Base
from database.orm._annotations import (
    IntegerPrimaryKey,
    BoolColumn,
    IntegerColumn,
    TextColumn,
    TimestampWTColumn,
)


class Organizations(Base):
    __tablename__ = "organizations"
    __table_args__ = (UniqueConstraint("name"),)
    id: Mapped[IntegerPrimaryKey] = mapped_column(Sequence("organizations_id_seq"))
    user_id: Mapped[IntegerColumn] = mapped_column(index=True, nullable=False)
    name: Mapped[TextColumn] = mapped_column(nullable=False)
    is_deleted: Mapped[BoolColumn] = mapped_column(
        index=True, nullable=False, default=False
    )
    created_at: Mapped[TimestampWTColumn] = mapped_column(
        nullable=True, default=func.now()
    )
