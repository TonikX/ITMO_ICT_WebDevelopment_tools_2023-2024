class DuplicatedLoginException(Exception):
    message = "Duplicated login. Please try again."

    def __str__(self):
        return self.message
