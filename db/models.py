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
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    markdown_file_path: Mapped[str] = mapped_column(String)
    banner_photo_path: Mapped[str] = mapped_column(String, nullable=True)
    create_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())


class Music(Base):
    __tablename__ = 'music'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, nullable=False, default='Без названия')
    artist: Mapped[str] = mapped_column(String, default='Неизвестен')
    duration: Mapped[str] = mapped_column(String, nullable=False)
    album: Mapped[str] = mapped_column(String, nullable=True)
    filename: Mapped[str] = mapped_column(String, nullable=False)


def init_db():
    with engine.begin() as conn:
        Base.metadata.create_all(bind=conn)
