from app.repository.mongo_repository import MongoRepository
from app.util.cryptography_util import CryptographyUtil
from app.mapper.user_mapper import UserMapper

class LoginService:
    def __init__(self):
        pass

    @staticmethod
    def login(credentials):
        user = credentials.get_user()
        password = credentials.get_password()
        repository = MongoRepository()
        user = repository.get_user(user)

        if user is None:
            return None

        if (CryptographyUtil.encrypt(password, user.get_password_salt()) != user.get_password_hash()):
            return None

        return True

    @staticmethod
    def list_users():
        repository = MongoRepository()
        return repository.list_users()