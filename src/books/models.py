from sqlmodel import SQLModel, Field
from sqlalchemy import Column, ForeignKey
from datetime import datetime, date
import sqlalchemy.dialects.postgresql as pg
import uuid
from typing import Optional


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

    def __repr__(self):
        return f"<Book {self.title}>"
