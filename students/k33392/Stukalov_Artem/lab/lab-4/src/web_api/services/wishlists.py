from sqlmodel import Session
from src.web_api.models import User
from src.web_api.services import books as books_service


def add_to_wishlist(session: Session, book_id: int, user: User) -> bool:
    book = books_service.get_book_by_id(session, book_id)
    if not book:
        return False

    user.wishlist.append(book)
    session.add(user)
    session.commit()
    session.refresh(user)
    return True


def remove_from_wishlist(session: Session, book_id: int, user: User) -> bool:
    count = len(user.wishlist)
    user.wishlist = list(filter(lambda book: book.id != book_id, user.wishlist))
    session.add(user)
    session.commit()
    session.refresh(user)
    return count != len(user.wishlist)
