import os
import redis
from flask import request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from .route_master import RouteMaster
from app.service.proposal_service import ProposalService

bp = RouteMaster.add_route('proposal', origins = ['*'])

@bp.route('/', methods=['GET'])
@jwt_required()
@RouteMaster.filter_input
def list_proposals():
    if (request.args.get('items') is not None):
        if (request.args.get('start') is not None):
            start = request.args.get('start')
        else:
            start = None

        proposals, end_value = ProposalService.listProposalsPaged(request.args.get('items'), start)

        if (proposals is None or len(proposals) == 0):
            return RouteMaster.not_found_response({'message': 'Proposals not found'})

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
    proposal = ProposalService.getProposal(id)
    if (proposal is None):
        return RouteMaster.not_found_response({'message': 'Proposal not found'})
    return RouteMaster.ok_response({'proposal': proposal})

@bp.route('/<id>', methods=['DELETE'])
@jwt_required()
def delete_proposal(id):
    if ProposalService.deleteProposal(id, get_jwt_identity()):
        return RouteMaster.ok_response({'message': 'Proposal deleted'})
    else:
        return RouteMaster.error_response({'message': 'Cant delete proposal or unauthorized'})

@bp.route('/', methods=['POST'])
@jwt_required()
def create_proposal():
    data = request.get_json()
    
    if (data is None):
        return RouteMaster.error_response({'message': 'Invalid request'})

    title = data.get('title', None)
    description = data.get('description', None)
    photos = data.get('photos', None)
    location = data.get('location', None)

    proposal = ProposalService.createProposal(title, description, photos, location, get_jwt_identity())
    if (proposal is None):
        return RouteMaster.error_response({'message': 'Invalid request'})
    
    return RouteMaster.created_response({'proposal': proposal})

@bp.route('/<id>', methods=['PUT'])
@jwt_required()
def update_proposal(id):
    data = request.get_json()

    if (data is None):
        return RouteMaster.error_response({'message': 'Invalid request'})

    title = data.get('title', None)
    description = data.get('description', None)
    photos = data.get('photos', None)

    proposal = ProposalService.updateProposal(id, title, description, photos, get_jwt_identity())
    if (proposal is None):
        return RouteMaster.error_response({'message': 'Invalid request'})
    
    return RouteMaster.ok_response({'likes': str(proposal)})

@bp.route('/like', methods=['GET'])
@jwt_required()
@RouteMaster.filter_input
def like_proposal():

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

    id = request.args.get('id')
    if (id is None):
        return RouteMaster.error_response({'message': 'Id required'})

    proposal = ProposalService.unlikeProposal(id, get_jwt_identity())
    if (proposal is None):
        return RouteMaster.error_response({'message': 'Invalid id or user token'})
    
    if (proposal == False):
        return RouteMaster.error_response({'message': 'Cant dislike a proposal you didnt like'})

    return RouteMaster.ok_response({'likes': str(proposal)})