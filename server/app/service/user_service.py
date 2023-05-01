from app.repository.mongo_repository import MongoRepository
from app.model.user_model import UserModel
from app.util.cryptography_util import CryptographyUtil
import time

class UserService:
    def __init__(self):
        pass

    @staticmethod
    def getUserByEmail(email):
        repository = MongoRepository()
        return UserModel.from_dict(repository.get_user_by_email(email))

    @staticmethod
    def getUserById(email):
        repository = MongoRepository()
        return UserModel.from_dict(repository.get_user(email))

    @staticmethod
    def updateUser(user, changes):
        repository = MongoRepository()
        return UserModel.from_dict(repository.update_user(user, changes))

    @staticmethod
    def registerUser(user):
        repository = MongoRepository()

        if (repository.get_user_by_email(user['email']) is not None):
            return None
        if (repository.get_user_by_dni(user['dni']) is not None):
            return None

        salt = CryptographyUtil.generate_salt()

        complete_user = {
            'name': user['name'],
            'email': user['email'],
            'dni': user['dni'],
            'photo': user['photo'],
            'verified': False,
            'public': user['public'],
            'password_hash': CryptographyUtil.encrypt(user['password'], salt),
            'password_salt': salt,
            'created_at': int(time.time()),
            'deleted_at': 0,
            'liked_proposals': [],
        }

        reponse_uid = repository.register_user(complete_user)
        return UserModel.from_dict(repository.get_user(reponse_uid))

    @staticmethod
    def deleteUser(user):
        repository = MongoRepository()
        user_model = UserService.getUserById(user)
        if user_model is None:
            return None
        if user_model.get_deleted_at() != 0:
            return None
            
        return repository.delete_user(user, int(time.time()))