import os
import redis
from flask import request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from .route_master import RouteMaster
from app.service.proposal_service import ProposalService
from app.service.user_service import UserService
from app.config import Config

bp = RouteMaster.add_route('proposal', origins = ['https://participasalvaterra.es'])

@bp.route('/', methods=['GET'])
@jwt_required()
@RouteMaster.filter_input
def list_proposals():
    user_id = get_jwt_identity()
    user = UserService.getUserById(user_id)
    if (user is None):
        return RouteMaster.unauthorized_response({'message': 'User not found'})

    if (request.args.get('items') is not None):
        if (request.args.get('start') is not None):
            start = request.args.get('start')
        else:
            start = None

        proposals, end_value = ProposalService.listProposalsPaged(request.args.get('items'), start)

        if (proposals is None or len(proposals) == 0):
            return RouteMaster.not_found_response({'message': 'Proposals not found'})

        if end_value is None:
            end_value = "-1"
            
        return RouteMaster.ok_response({'proposals': proposals, 'end': end_value})
    else:
        proposals = ProposalService.listProposals()

        if (proposals is None or len(proposals) == 0):
            return RouteMaster.not_found_response({'message': 'Proposals not found'})

        return RouteMaster.ok_response({'proposals': proposals})


@bp.route('/<id>', methods=['GET'])
@jwt_required()
@RouteMaster.filter_input
def get_proposal(id):
    user_id = get_jwt_identity()
    user = UserService.getUserById(user_id)
    if (user is None):
        return RouteMaster.unauthorized_response({'message': 'User not found'})

    proposal = ProposalService.getProposal(id)
    if (proposal is None):
        return RouteMaster.not_found_response({'message': 'Proposal not found'})
    return RouteMaster.ok_response({'proposal': proposal})

@bp.route('/<id>', methods=['DELETE'])
@jwt_required()
@RouteMaster.filter_input
def delete_proposal(id):
    user_id = get_jwt_identity()
    user = UserService.getUserById(user_id)
    if (user is None):
        return RouteMaster.unauthorized_response({'message': 'User not found'})

    if ProposalService.deleteProposal(id, get_jwt_identity()):
        return RouteMaster.ok_response({'message': 'Proposal deleted'})
    else:
        return RouteMaster.error_response({'message': 'Cant delete proposal or unauthorized'})

@bp.route('/', methods=['POST'])
@jwt_required()
@RouteMaster.filter_input
def create_proposal():
    user_id = get_jwt_identity()
    user = UserService.getUserById(user_id)
    if (user is None):
        return RouteMaster.unauthorized_response({'message': 'User not found'})

    data = request.get_json()
    
    if (data is None):
        return RouteMaster.error_response({'message': 'Invalid request'})

    try:
        title = data["title"]
        description = data["description"]
        photos = data["photos"]
        main_photo = data["main_photo"]
        location = data["coordinates"]
    except:
        return RouteMaster.error_response({'message': 'Invalid request'})

    proposal = ProposalService.createProposal(title, description, photos, main_photo, location, get_jwt_identity())
    if (proposal is None):
        return RouteMaster.error_response({'message': 'Invalid request'})
    
    return RouteMaster.created_response({'proposal': proposal})

@bp.route('/<id>', methods=['PUT'])
@jwt_required()
@RouteMaster.filter_input
def update_proposal(id):
    user_id = get_jwt_identity()
    user = UserService.getUserById(user_id)
    if (user is None):
        return RouteMaster.unauthorized_response({'message': 'User not found'})

    data = request.get_json()

    if (data is None):
        return RouteMaster.error_response({'message': 'Invalid request, no data'})

    title = data.get('title', None)
    description = data.get('description', None)
    photos = data.get('photos', None)
    main_photo = data.get('main_photo', None)


    proposal = ProposalService.updateProposal(id, title, description, photos, main_photo, get_jwt_identity())
    if (proposal is None):
        return RouteMaster.error_response({'message': 'Invalid request'})
    
    return RouteMaster.ok_response({'proposal': proposal.to_vo_dict()})

@bp.route('/like', methods=['GET'])
@jwt_required()
@RouteMaster.filter_input
def like_proposal():
    user_id = get_jwt_identity()
    user = UserService.getUserById(user_id)
    if (user is None):
        return RouteMaster.unauthorized_response({'message': 'User not found'})

    id = request.args.get('id')
    if (id is None):
        return RouteMaster.error_response({'message': 'Id required'})

    proposal = ProposalService.likeProposal(id, get_jwt_identity())
    if (proposal is None):
        return RouteMaster.error_response({'message': 'Invalid id or user token'})
    
    if (proposal == False):
        return RouteMaster.error_response({'message': 'Cant like proposal twice'})

    return RouteMaster.ok_response({'likes': str(proposal)})

@bp.route('/dislike', methods=['GET'])
@jwt_required()
@RouteMaster.filter_input
def unlike_proposal():
    user_id = get_jwt_identity()
    user = UserService.getUserById(user_id)
    if (user is None):
        return RouteMaster.unauthorized_response({'message': 'User not found'})
        
    id = request.args.get('id')
    if (id is None):
        return RouteMaster.error_response({'message': 'Id required'})

    proposal = ProposalService.unlikeProposal(id, get_jwt_identity())
    if (proposal is None):
        return RouteMaster.error_response({'message': 'Invalid id or user token'})
    
    return RouteMaster.ok_response({'likes': str(proposal)})