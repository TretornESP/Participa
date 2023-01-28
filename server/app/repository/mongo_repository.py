from app.config import Config
from pymongo import MongoClient
from bson import ObjectId

class MongoRepository:
    def __init__(self):
        cfg = Config()
        self.config = cfg.toDict()['mongo']
        self.log = cfg.log
        self.connstring = self.config['connstring']
        self.client = MongoClient(self.connstring)
        self.users_collection = self.client[self.config['database']][self.config['user_collection']]
        self.proposals_collection = self.client[self.config['database']][self.config['proposal_collection']]
        self.photos_collection = self.client[self.config['database']][self.config['photo_collection']]
        
    def list_users(self):
        return self.users_collection.find()

    def get_user(self, username):
        return self.users_collection.find_one({'email': username})

    def update_user(self, user, changes):
        self.users_collection.update_one({'email': user}, {'$set': changes})
        return self.get_user(user)

    def get_proposal(self, proposal_id):
        return self.proposals_collection.find_one({'_id': ObjectId(proposal_id)})

    def list_proposals(self):
        return self.proposals_collection.find()

    def list_proposals_paged(self, start_value, items_per_page):
        if start_value is None:
            proposals = self.proposals_collection.find().sort('_id',-1 ).limit(int(items_per_page))
            start_value = proposals[0]['_id']
        return self.proposals_collection.find({ '_id': { '$lt': ObjectId(start_value) } } ).sort('_id',-1).limit(int(items_per_page))

    def create_proposal(self, proposal):
        id = self.proposals_collection.insert_one(proposal).inserted_id
        return self.get_proposal(id)

    def delete_proposal(self, proposal_id):
        self.proposals_collection.delete_one({'_id': ObjectId(proposal_id)})

    def update_proposal(self, proposal_id, changes):
        self.proposals_collection.update_one({'_id': ObjectId(proposal_id)}, {'$set': changes})
        return self.get_proposal(proposal_id)

    def upload_photo(self, photo):
        return self.photos_collection.insert_one(photo).inserted_id