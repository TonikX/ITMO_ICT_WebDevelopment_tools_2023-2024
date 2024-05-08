
class InvalidUsernameException(Exception):
    message = "Invalid username. Should be between 5 and 30 characters long."

    def __str__(self):
        return self.message


class InvalidUserLoginException(Exception):
    message = "Invalid login. Should be between 5 and 30 characters long."

    def __str__(self):
        return self.message

