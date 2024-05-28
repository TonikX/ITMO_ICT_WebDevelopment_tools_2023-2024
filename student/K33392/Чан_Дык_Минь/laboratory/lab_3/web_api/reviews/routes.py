from web_api.connection import init_db, get_session
from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlmodel import select 
from web_api.models import *
from typing_extensions import TypedDict
from web_api.auth.auth import AuthHandler
from uuid import UUID

router = APIRouter()
auth_handler = AuthHandler()

# Reviews endpoints

@router.get('/reviews', tags=["reviews"], response_model=List[UserReview])
def get_user_reviews(current_user: User = Depends(auth_handler.get_current_user),
                     session=Depends(get_session)) -> List[UserReview]:
    # Query the database for reviews associated with the current user
    user_reviews = session.query(UserReview).filter(UserReview.user_profile == current_user.user_profile).all()
    
    # Check if any reviews were found
    if not user_reviews:
        raise HTTPException(status_code=404, detail="No reviews found for the current user")
    
    return user_reviews

@router.get('/review/{user_profile_id}', tags=["reviews"])
def review_get(user_profile_id: UUID, session=Depends(get_session)) -> List[UserReview]:
    review = session.query(UserReview).filter(UserReview.user_profile_id == user_profile_id).all()
    return review

@router.post('/review/{user_profile_id}', tags=["reviews"])
def review_create(user_profile_id: UUID,
                  review: UserReviewDefault, 
                  current_user: User = Depends(auth_handler.get_current_user),
                  session=Depends(get_session)) -> TypedDict('Response', {"status": int, "data": UserReview}): # type: ignore

    # Assign the current user's ID to the profile
    review_dict = review.dict()
    review_dict["user_profile_id"] = user_profile_id
    review_dict["reviewer"] = current_user.username
    review_dict["review_time"] = date.today()

    # Create a new profile instance with the assigned user_id
    review_instance = UserReview(**review_dict)

    session.add(review_instance)
    session.commit()
    session.refresh(review_instance)
    
    return {"status": 200, "data": review_instance}

@router.delete('/review/delete{review_id}', tags=["reviews"])
def review_delete(review_id: UUID, 
                  current_user: User = Depends(auth_handler.get_current_user), 
                  session=Depends(get_session)):
    review = session.get(UserReview, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    session.delete(review)
    session.commit()
    return {"ok": True}

@router.patch("/review{review_id}", tags=["reviews"])
def review_update(review_id: UUID, 
                  review: UserReviewDefault, 
                  current_user: User = Depends(auth_handler.get_current_user),
                  session=Depends(get_session)) -> UserReviewDefault:
                  
    db_review = session.get(UserReview, review_id)
    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found")
    review_data = review.model_dump(exclude_unset=True)
    for key, value in review_data.items():
        setattr(db_review, key, value)
    session.add(db_review)
    session.commit()
    session.refresh(db_review)
    return db_review