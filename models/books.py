from sqlalchemy.orm import Mapped, mapped_column

from database import Model


class BooksModel(Model):
    __tablename__ = "books"
    
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    title: Mapped[str] = mapped_column(nullable=False)
    author: Mapped[str] = mapped_column(nullable=False)
    year: Mapped[int]
    pages: Mapped[int]
    is_read: Mapped[bool] = mapped_column(default=False)
    