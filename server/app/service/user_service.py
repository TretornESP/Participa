from app.repository.mongo_repository import MongoRepository

class UserService:
    def __init__(self):
        pass

    @staticmethod
    def getUser(email):
        repository = MongoRepository()
        return repository.get_user(email)

    @staticmethod
    def updateUser(user, changes):
        repository = MongoRepository()
        return repository.update_user(user, changes)