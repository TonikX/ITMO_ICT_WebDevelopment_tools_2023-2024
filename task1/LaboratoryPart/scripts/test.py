from endpoints import endpoint_tools as tools
from db import get_session_func
import models

class A:
    def _do(self):
        self._print_str()

    def _print_str(self):
        print('A')


class B(A):
    def _do(self):
        super(B, self)._do()

    def _print_str(self):
        print('B')


if __name__ == '__main__':
    # B()._do()
    with get_session_func() as session:
        validator = tools.TaskValidator(session,1, 1)
        task: models.Task = validator.object
        print(task)


    with get_session_func() as session:
        validator = tools.CategoryValidator(session,1, 1)
        category = validator.object
        print(category)


