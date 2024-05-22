from typing import Callable, Any

from personal_finance.application.users.service import UserService
from personal_finance.infrastructure.persistance.postgres.database import get_session
from personal_finance.infrastructure.persistance.postgres.users.repository import UserRepository


class IocContainer:

    repository: dict[str, Callable[[], Any]] = {
            "UserRepository": lambda: UserRepository(next(get_session()))
        }

    service: dict[str, Callable[[], Any]] = {
            "UserService": lambda: UserService(IocContainer.repository['UserRepository']())
        }
