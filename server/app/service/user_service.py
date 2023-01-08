from app.repository.mongo_repository import MongoRepository
from app.model.user_model import UserModel
class UserService:
    def __init__(self):
        pass

    @staticmethod
    def getUser(email):
        repository = MongoRepository()
        return UserModel.from_dict(repository.get_user(email))

    @staticmethod
    def updateUser(user, changes):
        repository = MongoRepository()
        return UserModel.from_dict(repository.update_user(user, changes))