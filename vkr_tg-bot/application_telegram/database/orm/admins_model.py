from sqlalchemy.orm import Mapped, mapped_column

from database.orm._base_class import Base
from database.orm._annotations import (
    IntegerPrimaryKey,
    TextColumn,
    BoolColumn
)

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Admins(Base):
    __tablename__ = "admins"
    id: Mapped[IntegerPrimaryKey] = mapped_column(autoincrement=True, primary_key=True, unique=True, nullable=False)
    username: Mapped[TextColumn] = mapped_column(nullable=False, unique=True)
    password: Mapped[TextColumn] = mapped_column(nullable=False)
    is_superadmin: Mapped[BoolColumn] = mapped_column()

    def set_password(self, password_plain) -> None:
        self.password = pwd_context.hash(password_plain)

    def check_password(self, password_plain) -> bool:
        return pwd_context.verify(secret=password_plain, hash=self.password)
