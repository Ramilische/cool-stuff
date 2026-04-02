from datetime import datetime
from typing import List

from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Integer, ARRAY, Boolean, Text, DateTime

from db.session import engine


class Base(DeclarativeBase):
    pass


class Post(Base):
    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    markdown_file_path: Mapped[str] = mapped_column(String)
    banner_photo_path: Mapped[str] = mapped_column(String, nullable=True)
    create_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())


def init_db():
    with engine.begin() as conn:
        Base.metadata.create_all(bind=conn)
