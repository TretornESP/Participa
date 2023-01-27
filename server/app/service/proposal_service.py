import time
from app.repository.mongo_repository import MongoRepository
from app.model.proposal_model import ProposalModel

class ProposalService:
    def __init__(self):
        pass

    @staticmethod
    def getProposal(id):
        repository = MongoRepository()
        proposal = repository.get_proposal(id)
        if (proposal is None):
            return None
        return ProposalModel.from_dict(proposal).to_vo_dict()

    @staticmethod
    def listProposals():
        repository = MongoRepository()
        proposals = []
        for proposal in repository.list_proposals():
            proposals.append(ProposalModel.from_dict(proposal).to_vo_dict())
        return proposals

    @staticmethod
    def listProposalsPaged(items, handler=None):
        repository = MongoRepository()
        proposals = []
        count = 0
        proposals_raw = repository.list_proposals_paged(start_value=handler, items_per_page=items)

        for proposal in proposals_raw:
            proposals.append(ProposalModel.from_dict(proposal).to_vo_dict())
            print(proposal)
            count += 1

        end_value = None
        if count == int(items):
            end_value = proposals[len(proposals)-1]['id']

        return proposals, end_value

    @staticmethod
    def createProposal(title, description, photos, location, author):
        repository = MongoRepository()
        
        data = {
            "title": title,
            "description": description,
            "photos": photos,
            "coordinates": location,
            "author": author,
            "likes": 0,
            "created_at": int(time.time())
        }
        proposal_model = ProposalModel.from_dict(data)

        proposal = repository.create_proposal(proposal_model.to_dict())

        if (proposal is None):
            return None
        
        return ProposalModel.from_dict(proposal).to_vo_dict()

    @staticmethod
    def deleteProposal(id, user):
        repository = MongoRepository()
        proposal = repository.get_proposal(id)
        if (proposal is None):
            return None
        if (proposal['author'] != user):
            return None
        
        repository.delete_proposal(id)

        proposal = repository.get_proposal(id)
        if (proposal is not None):
            return None

        return True

    @staticmethod
    def updateProposal(id, title, description, photos, author):
        repository = MongoRepository()
        proposal = repository.get_proposal(id)
        if (proposal is None):
            return None
        if (proposal['author'] != author):
            return None

        changes = {}
        if (title is not None):
            changes['title'] = title
        if (description is not None):
            changes['description'] = description
        if (photos is not None):
            changes['photos'] = photos
        
        return ProposalModel.from_dict(repository.update_proposal(id, changes))

    @staticmethod
    def likeProposal(id, user):
        repository = MongoRepository()
        user_data = repository.get_user(user)
        proposal = repository.get_proposal(id)

        if (proposal is None):
            return None

        if (user_data is None):
            return None
        
        if id in user_data["liked_proposals"]:
            return False

        user_data["liked_proposals"].append(id)
        proposal['likes'] += 1

        repository.update_user(user, user_data)
        repository.update_proposal(id, proposal)

        return proposal['likes']

    @staticmethod
    def unlikeProposal(id, user):
        repository = MongoRepository()
        user_data = repository.get_user(user)
        proposal = repository.get_proposal(id)

        if (proposal is None):
            return None

        if (user_data is None):
            return None
        
        if id not in user_data["liked_proposals"]:
            return False

        user_data["liked_proposals"].remove(id)
        proposal['likes'] -= 1

        repository.update_user(user, user_data)
        repository.update_proposal(id, proposal)

        return proposal['likes']