from app.repository.mongo_repository import MongoRepository
from app.util.cryptography_util import CryptographyUtil
from app.model.user_model import UserModel

class LoginService:
    def __init__(self):
        pass

    @staticmethod
    def login(user, password):

        repository = MongoRepository()
        user = UserModel.from_dict(repository.get_user(user))

        if user is None:
            return False

        if (CryptographyUtil.encrypt(password, user.get_password_salt()) != user.get_password_hash()):
            return False

        return True