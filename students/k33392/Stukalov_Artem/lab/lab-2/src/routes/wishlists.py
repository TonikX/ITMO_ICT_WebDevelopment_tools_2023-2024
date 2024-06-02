from fastapi import APIRouter, Depends
from src.models import User, WishlistAdd, WishlistRemove
from src.config import db
from src.services import auth as auth_service, wishlists as wishlist_service
from sqlmodel import Session

router = APIRouter()


@router.post("/")
def add_to_wishlist(
    wishlist_add: WishlistAdd,
    session: Session = Depends(db.get_session),
    current_user: User = Depends(auth_service.get_current_user),
) -> bool:
    was_added = wishlist_service.add_to_wishlist(
        session=session, book_id=wishlist_add.book_id, user=current_user
    )
    return was_added


@router.delete("/")
def remove_from_wishlist(
    wishlist_remove: WishlistRemove,
    session: Session = Depends(db.get_session),
    current_user: User = Depends(auth_service.get_current_user),
) -> bool:
    was_removed = wishlist_service.remove_from_wishlist(
        session=session, book_id=wishlist_remove.book_id, user=current_user
    )
    return was_removed
