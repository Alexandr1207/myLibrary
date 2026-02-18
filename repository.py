from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from models.books import BooksModel
from schemas.books import SBookAdd, SBook


class BookRepository:
    @classmethod
    async def add_one(cls, data: SBookAdd, session: AsyncSession):
        book_dict = data.model_dump()
        
        book = BooksModel(**book_dict)
        
        session.add(book)
        await session.commit()
        await session.refresh(book)
        
        return book
    
    @classmethod
    async def find_all(cls, session: AsyncSession):
        query = select(BooksModel)
        
        result = await session.execute(query)
        books_models = result.scalars().all()
        return books_models
    
    @classmethod
    async def find_by_id(cls, book_id: int, session: AsyncSession):
        query = select(BooksModel).where(BooksModel.id == book_id)
        
        result = await session.execute(query)
        books_model = result.scalar_one_or_none()
        
        if not books_model:
            return None
        
        return books_model
    
    @classmethod
    async def del_one(cls, book_id: int, session: AsyncSession):
        book = await cls.find_by_id(book_id, session)
        if book:
            await session.delete(book)
            await session.commit()
            return 1
        return None
    
    @classmethod
    async def update_one(cls, book_id: int, data: SBookAdd, session: AsyncSession):
        update_data = data.model_dump(exclude_unset=True)
        
        query = (
            update(BooksModel)
            .where(BooksModel.id == book_id)
            .values(**update_data)
            .returning(BooksModel)
        )
        
        result = await session.execute(query)
        await session.commit()
        
        updated_book = result.scalar_one_or_none()
        
        if not updated_book:
            return None
        
        return updated_book
