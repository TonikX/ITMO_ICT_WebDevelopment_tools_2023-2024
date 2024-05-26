import models
from db import get_session_func
import sqlmodel
import typing as tp




def get_user_by_username(username: str) -> models.User:
    with get_session_func() as session:
        select_statement = \
            sqlmodel.select(models.User).\
            where(models.User.username == username)
        user = session.exec(select_statement).one_or_none()
    if user is None:
        raise ValueError('no user with such username')
    return user



# def get_project_calendar_entries(
#
# )

# def get_category_calendar_entries(
#         session: sqlmodel.Session,
#         category_id:int
# ) -> tp.List[models.CalendarEntry]:
#
# def get_task_calendar_entries(
#         session: sqlmodel.Session,
#         task_id:int
# ) -> tp.List[models.CalendarEntry]:
#     pass
