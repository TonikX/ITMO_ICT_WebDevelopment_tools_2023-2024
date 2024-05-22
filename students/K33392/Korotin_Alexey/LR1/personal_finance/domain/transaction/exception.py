class TransactionCommentException(Exception):
    message: str

    def __init__(self, message: str) -> None:
        self.message = message


class TransactionExecutionException(Exception):
    message: str

    def __init__(self, message: str) -> None:
        self.message = message


class TagNameException(Exception):
    message: str

    def __init__(self, message: str) -> None:
        self.message = message
