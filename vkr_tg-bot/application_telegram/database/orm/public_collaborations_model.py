from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func, Sequence, UniqueConstraint, ForeignKeyConstraint

from database.orm._base_class import Base
from database.orm._annotations import (
    IntegerPrimaryKey,
    TextColumn,
    TimestampWTColumn,
    IntegerColumn,
    BoolColumn,
)


class Collaborations(Base):
    __tablename__ = "collaborations"
    __table_args__ = (
        UniqueConstraint("name"),
        ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
    )
    id: Mapped[IntegerPrimaryKey] = mapped_column(Sequence("collaborations_id_seq"))
    user_id: Mapped[IntegerColumn] = mapped_column(index=True, nullable=False)
    name: Mapped[TextColumn] = mapped_column(nullable=False)
    uuid_name: Mapped[TextColumn] = mapped_column(nullable=False)
    created_at: Mapped[TimestampWTColumn] = mapped_column(
        nullable=True, default=func.now()
    )
