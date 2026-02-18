from fastapi import APIRouter, HTTPException, status

from database import SessionDep
from repository import BookRepository
from schemas.books import SBook, SBookAdd

router = APIRouter(
    prefix="/books",
    tags=["Книги"]
)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=SBook)
async def create_book(book: SBookAdd, session: SessionDep):
    book_model = await BookRepository.add_one(book, session)
    return book_model


@router.get("", status_code=status.HTTP_200_OK, response_model=list[SBook])
async def get_books(session: SessionDep):
    books = await BookRepository.find_all(session)
    return books


@router.get("/{book_id}", status_code=status.HTTP_200_OK, response_model=SBook)
async def get_book_by_id(book_id: int, session: SessionDep):
    book_model = await BookRepository.find_by_id(book_id, session)
    if not book_model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book_model


@router.put("/{book_id}", status_code=status.HTTP_200_OK, response_model=SBook)
async def update_book(book_id: int, new_book: SBookAdd, session: SessionDep):
    book = await BookRepository.update_one(book_id, new_book, session)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def del_book(book_id: int, session: SessionDep):
    result = await BookRepository.del_one(book_id, session)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return {"message": "ok"}