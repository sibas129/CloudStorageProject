from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func, Sequence, UniqueConstraint

from database.orm._base_class import Base
from database.orm._annotations import (
    IntegerPrimaryKey,
    BigintColumn,
    TextColumn,
    TimestampWTColumn,
)


class Users(Base):
    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("telegram_id"),)
    id: Mapped[IntegerPrimaryKey] = mapped_column(Sequence("users_id_seq"))
    telegram_id: Mapped[BigintColumn] = mapped_column(index=True, nullable=False)
    telegram_name: Mapped[TextColumn] = mapped_column(nullable=True)
    created_at: Mapped[TimestampWTColumn] = mapped_column(
        nullable=True, default=func.now()
    )
    updated_at: Mapped[TimestampWTColumn] = mapped_column(
        nullable=True, default=func.now(), onupdate=func.now()
    )
