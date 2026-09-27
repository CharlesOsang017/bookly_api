from sqlmodel import SQLModel, Field, Column, Relationship
from datetime import datetime, date
import sqlalchemy.dialects.postgresql as pg
import uuid
from typing import List

# from src.db import models
from sqlalchemy import Column, ForeignKey
from typing import Optional
from src.db import models


class User(SQLModel, table=True):
    __tablename__ = "Users"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    username: str
    email: str
    password_hash: str = Field(exclude=True)
    first_name: str
    last_name: str
    role: str = Field(
        sa_column=Column(pg.VARCHAR, nullable=False, server_default="user")
    )
    is_verified: bool = False
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    books: List["models.Book"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )

    def __repr__(self):
        return f"<User {self.username}>"


class Book(SQLModel, table=True):
    __tablename__ = "books"
    uuid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False
        )
    )
    title: str = Field(index=True)
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
    user_uid: Optional[uuid.UUID] = Field(
        default=None,
        sa_column=Column(
            pg.UUID,
            ForeignKey("Users.uid"),
            nullable=True,
        ),
    )
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    user: Optional["models.User"] = Relationship(back_populates="books")

    def __repr__(self):
        return f"<Book {self.title}>"


class Review(SQLModel, table=True):
    __tablename__ = "reviews"
    uuid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False
        )
    )
    user_uid: Optional[uuid.UUID] = Field(
        default=None,
        sa_column=Column(
            pg.UUID,
            ForeignKey("Users.uid"),
            nullable=True,
        ),
    )
    book_uid: Optional[uuid.UUID] = Field(
        default=None,
        sa_column=Column(
            pg.UUID,
            ForeignKey("books.uid"),
            nullable=True,
        ),
    )
    rating: int = Field(lte=5)
    review_text: str
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    user: Optional["models.User"] = Relationship(back_populates="books")

    def __repr__(self):
        return f"<Review for book {self.book_uid} by user {self.user_uid}>"
