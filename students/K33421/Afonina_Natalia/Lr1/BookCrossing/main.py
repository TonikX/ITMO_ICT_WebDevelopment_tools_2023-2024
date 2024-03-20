from fastapi import FastAPI, HTTPException, status
from typing import List
from models import *

app = FastAPI()

temp_bd = [
    {
        "user_profiles": [
            {
                "id": 1,
                "username": "user1",
                "firstname": "John",
                "lastname": "Doe",
                "age": 30,
                "location": "New York",
                "bio": "User 1 bio"
            },
            {
                "id": 2,
                "username": "user2",
                "firstname": "Jane",
                "lastname": "Smith",
                "age": 25,
                "location": "Los Angeles",
                "bio": "User 2 bio"
            }
        ],
        "books": [
            {
                "id": 1,
                "title": "Book 1",
                "author_id": {"id": 1, "name": "Author 1", "bio": "Author 1 bio"},
                "genre": "fiction",
                "bio": "Book 1 bio"
            },
            {
                "id": 2,
                "title": "Book 2",
                "author_id": {"id": 2, "name": "Author 2", "bio": "Author 2 bio"},
                "genre": "non-fiction",
                "bio": "Book 2 bio"
            }
        ],
        "book_reviews": [
            {
                "id": 1,
                "book_id": {"id": 1, "title": "Book 1",
                            "author_id": {"id": 1, "name": "Author 1", "bio": "Author 1 bio"},
                            "genre": "fiction", "bio": "Book 1 bio"},
                "reviewer_id": {"id": 1, "username": "user1", "firstname": "John", "lastname": "Doe", "age": 30,
                                "location": "New York", "bio": "User 1 bio"},
                "rating": 4,
                "review_text": "Interesting book."
            },
            {
                "id": 2,
                "book_id": {"id": 2, "title": "Book 2",
                            "author_id": {"id": 2, "name": "Author 2", "bio": "Author 2 bio"},
                            "genre": "non-fiction", "bio": "Book 2 bio"},
                "reviewer_id": {"id": 2, "username": "user2", "firstname": "Jane", "lastname": "Smith", "age": 25,
                                "location": "Los Angeles", "bio": "User 2 bio"},
                "rating": 3,
                "review_text": "Good read."
            }
        ]
    }
]


@app.get("/users_list")
def users_list() -> List[UserProfile]:
    users = [user_data for data in temp_bd for user_data in data.get("user_profiles", [])]
    return users


@app.get("/user/{user_id}")
def get_user(user_id: int) -> UserProfile:
    for data in temp_bd:
        for user_data in data.get("user_profiles", []):
            if user_data.get("id") == user_id:
                return user_data
    raise HTTPException(status_code=404, detail="User not found")


@app.post("/user")
def create_user(user: UserProfile):
    for data in temp_bd:
        if "user_profiles" in data:
            data["user_profiles"].append(user.dict())
            return {"message": "User added successfully"}


@app.delete("/user/user{user_id}")
def delete_user(user_id: int):
    for data in temp_bd:
        for user_data in data.get("user_profiles", []):
            if user_data.get("id") == user_id:
                data["user_profiles"].remove(user_data)
                return {"status": 201, "message": "User deleted successfully"}
    raise HTTPException(status_code=404, detail="User not found")


@app.put("/user{user_id}")
def update_user(user_id: int, user_update: UserProfile):
    for data in temp_bd:
        for user_data in data.get("user_profiles", []):
            if user_data.get("id") == user_id:
                user_data.update(user_update.dict())
                return {"message": "User updated successfully"}
    raise HTTPException(status_code=404, detail="User not found")


@app.get("/book_list")
def book_list() -> List[Book]:
    books = [book_data for data in temp_bd for book_data in data.get("books", [])]
    return books


@app.get("/book/{book_id}")
def get_book(book_id: int) -> Book:
    for data in temp_bd:
        for book_data in data.get("books", []):
            if book_data.get("id") == book_id:
                return book_data
    raise HTTPException(status_code=404, detail="Book not found")


@app.post("/book")
def create_book(book: Book):
    for data in temp_bd:
        if "books" in data:
            data["books"].append(book.dict())
            return {"status": 200, "data": book, "message": "Book added successfully"}


@app.put("/book/{book_id}")
def update_book(book_id: int, book_update: Book):
    for data in temp_bd:
        for book_data in data.get("books", []):
            if book_data.get("id") == book_id:
                book_data.update(book_update.dict())
                return {"message": "Book updated successfully"}
    raise HTTPException(status_code=404, detail="Book not found")


def get_all_book_reviews() -> List[BookReview]:
    reviews = [review_data for data in temp_bd for review_data in data.get("book_reviews", [])]
    return reviews


@app.get("/book_review/{review_id}")
def get_book_review(review_id: int) -> BookReview:
    for data in temp_bd:
        for review_data in data.get("book_reviews", []):
            if review_data.get("id") == review_id:
                return review_data
    raise HTTPException(status_code=404, detail="Book review not found")


@app.post("/book_review")
def create_book_review(review: BookReview):
    for data in temp_bd:
        if "book_reviews" in data:
            data["book_reviews"].append(review.dict())
            return review
    raise HTTPException(status_code=404, detail="Book reviews not found")


@app.put("/book_review/{review_id}")
def update_book_review(review_id: int, review_update: BookReview):
    for data in temp_bd:
        if "book_reviews" in data:
            for review_data in data["book_reviews"]:
                if review_data["id"] == review_id:
                    review_data.update(review_update.dict())
                    return review_update
    raise HTTPException(status_code=404, detail="Book review not found")


@app.delete("/book_review/{review_id}")
def delete_book_review(review_id: int):
    for data in temp_bd:
        if "book_reviews" in data:
            for review_data in data["book_reviews"]:
                if review_data["id"] == review_id:
                    data["book_reviews"].remove(review_data)
                    return {"message": "Book review deleted successfully"}
    raise HTTPException(status_code=404, detail="Book review not found")
