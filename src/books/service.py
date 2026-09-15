from src.books.schemas import BookUpdateModel, BookCreateModel

from sqlmodel.ext.asyncio.session import AsyncSession

from sqlmodel import select, desc
from .models import Book
from datetime import datetime


class BookService:
    async def get_all_books(self, session: AsyncSession):
        statement = select(Book).order_by(desc(Book.created_at))
        result = await session.exec(statement)
        return result.all()

    async def get_book(self, book_uid: str, session: AsyncSession):
        statement = select(Book).where(Book.uuid == book_uid)
        result = await session.exec(statement)
        return result.first()

    async def create_book(self, book_data: BookCreateModel, session: AsyncSession):
        book_data_dict = book_data.model_dump()

        new_book = Book(**book_data_dict)
        session.add(new_book)
        await session.commit()

        return new_book

    async def update_book(
        self, book_uid: str, update_book_data: BookUpdateModel, session: AsyncSession
    ):
        book_to_update = await self.get_book(book_uid, session)

        if book_to_update is not None:
            update_data_dict = update_book_data.model_dump(exclude_unset=True)

            for key, value in update_data_dict.items():
                if hasattr(book_to_update, key) and value is not None:
                    setattr(book_to_update, key, value)
            book_to_update.updated_at = datetime.now()
            await session.commit()
            return book_to_update
        else:
            return None

    async def delete_book(self, book_uid: str, session: AsyncSession):
        book_to_delete = await self.get_book(book_uid, session)

        if book_to_delete is not None:
            await session.delete(book_to_delete)
            await session.commit()
            return True
        else:
            return None
