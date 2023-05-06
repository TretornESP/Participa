import time
from app.repository.mongo_repository import MongoRepository
from app.model.proposal_model import ProposalModel
from app.controller.route_master import RouteMaster

class ProposalService:
    def __init__(self):
        pass

    @staticmethod
    def getProposal(id):
        repository = MongoRepository()
        proposal = repository.get_proposal(id)
        if (proposal is None):
            return None
        if (proposal['deleted_at'] != 0):
            return None

        return ProposalModel.from_dict(proposal).to_vo_dict()

    @staticmethod
    def listProposals():
        repository = MongoRepository()
        proposals = []
        for proposal in repository.list_proposals():
            if proposal['deleted_at'] == 0:
                proposals.append(ProposalModel.from_dict(proposal).to_vo_dict())
        return proposals

    @staticmethod
    def listProposalsPaged(items, handler=None):
        repository = MongoRepository()
        proposals = []
        count = 0
        proposals_raw = repository.list_proposals_paged(start_value=handler, items_per_page=items)

        for proposal in proposals_raw:
            if proposal['deleted_at'] == 0:
                proposals.append(ProposalModel.from_dict(proposal).to_vo_dict())
                count += 1

        end_value = None
        if count == int(items):
            end_value = proposals[len(proposals)-1]['id']

        return proposals, end_value

    @staticmethod
    def createProposal(title, description, photos, main_photo, location, author):
        repository = MongoRepository()

        existing = repository.get_proposal_by_title(title)
        if (existing is not None):
            return None
        
        data = {
            "title": title,
            "description": description,
            "photos": photos,
            "main_photo": main_photo,
            "coordinates": location,
            "author": author,
            "likes": 0,
            "created_at": int(time.time()),
            "deleted_at": 0,
        }

        proposal_model = ProposalModel.from_dict(data)

        proposal = repository.create_proposal(proposal_model.to_creation_dict())

        if (proposal is None):
            return None
        
        return ProposalModel.from_dict(proposal).to_vo_dict()

    @staticmethod
    def deleteProposal(id, user):
        repository = MongoRepository()
        proposal = ProposalModel.from_dict(repository.get_proposal(id))
        if (proposal is None):
            return None
        if (proposal.get_deleted_at() != 0):
            return None
        if (proposal.get_author() != user):
            return None
        
        repository.delete_proposal(id, int(time.time()))

        proposal = repository.get_proposal(id)
        if (proposal['deleted_at'] == 0):
            return None

        return True

    @staticmethod
    def updateProposal(id, title, description, photos, main_photo, author):
        repository = MongoRepository()
        proposal = repository.get_proposal(id)
        if (proposal is None):
            RouteMaster.log("Proposal not found")
            return None
        if (str(proposal['author']) != str(author)):
            RouteMaster.log("User not authorized to update proposal (user: " + str(author) + ", proposal: " + str(proposal['author']) + ")")
            return None

        changes = {}
        if (title is not None):
            changes['title'] = title
        if (description is not None):
            changes['description'] = description
        if (photos is not None):
            changes['photos'] = photos
        if (main_photo is not None):
            changes['main_photo'] = main_photo
        
        return ProposalModel.from_dict(repository.update_proposal(id, changes))

    @staticmethod
    def likeProposal(id, user):
        repository = MongoRepository()
        RouteMaster.log("Like proposal, id: " + id + ", user: " + user)
        user_data = repository.get_user(user)
        proposal = repository.get_proposal(id)

        if (proposal is None):
            RouteMaster.log("Proposal not found")
            return None

        if (user_data is None):
            RouteMaster.log("User not found")
            return None
        
        if id in user_data["liked_proposals"]:
            RouteMaster.log("User already liked this proposal")
            return False

        user_data["liked_proposals"].append(id)
        proposal['likes'] += 1

        repository.update_user(user, user_data)
        repository.update_proposal(id, proposal)

        return proposal['likes']

    @staticmethod
    def unlikeProposal(pid, user):
        repository = MongoRepository()
        user_data = repository.get_user(user)
        proposal = repository.get_proposal(pid)

        if (proposal is None):
            return None

        if (user_data is None):
            return None
        
        if pid not in user_data["liked_proposals"]:
            return None

        user_data["liked_proposals"].remove(pid)
        proposal['likes'] -= 1

        repository.update_user(user, user_data)
        repository.update_proposal(pid, proposal)

        return proposal['likes']