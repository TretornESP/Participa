from app.config import Config
from app.mapper.user_mapper import UserMapper
from pymongo import MongoClient

class MongoRepository:
    def __init__(self):
        cfg = Config()
        self.config = cfg.toDict()['mongo']
        self.log = cfg.log
        self.connstring = self.config['connstring']
        self.client = MongoClient(self.connstring)
        self.users_collection = self.client[self.config['database']][self.config['user_collection']]

    def list_users(self):
        users = []
        for user in self.users_collection.find():
            users.append(UserMapper.repository_to_model(user))
        return users

    def get_user(self, username):
        user = self.users_collection.find_one({'email': username})
        if user is None:
            return None
        return UserMapper.repository_to_model(user)