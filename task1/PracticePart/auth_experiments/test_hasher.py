from passlib.context import CryptContext

class PasswordHandler:
    crypto_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

    def verify_password(self, provided_password, actual_hash):
        return self.crypto_context.verify(provided_password, actual_hash)

    def get_password_hash(self, password):
        return self.crypto_context.hash(password)


if __name__ == '__main__':
    handler = PasswordHandler()
    password = '123456'
    hash = handler.get_password_hash('123456')
    print(handler.verify_password(password, hash))
