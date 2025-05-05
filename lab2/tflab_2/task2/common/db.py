from tflab_2.task2.common.connection import get_session
from tflab_2.task2.common.models import Gender, User


def save_user(user_data: dict):
    with next(get_session()) as session:
        user = User(
            name=user_data["name"],
            email=user_data["email"],
            password=user_data["password"],
            age=user_data.get("age"),
            country=user_data.get("country"),
            bio=user_data.get("bio"),
            gender=Gender(user_data["gender"]) if user_data.get("gender") else None,
        )
        session.add(user)
        session.commit()
        session.refresh(user)
