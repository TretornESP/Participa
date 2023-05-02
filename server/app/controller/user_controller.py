import os
import redis
from flask import request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity

from .route_master import RouteMaster
from app.service.user_service import UserService

bp = RouteMaster.add_route('user', origins = ['https://localhost'])

@bp.route('/', methods=['GET'])
@jwt_required()
def get_user():
     current_user_id = get_jwt_identity()
     user = UserService.getUserById(current_user_id)
     if (user is None):
         return RouteMaster.not_found_response({'message': 'User not found'})
     return RouteMaster.ok_response({'user': user.to_vo_dict()})

@bp.route('/', methods=['PUT'])
@jwt_required()
@RouteMaster.filter_input
def update_user():
    user_id = get_jwt_identity()
    user = UserService.getUser(user_id)
    if (user is None):
        return RouteMaster.unauthorized_response({'message': 'User not found'})

    current_user_id = get_jwt_identity()
    RouteMaster.log('Updating user: ' + str(current_user_id) + ' with changes: ' + str(request.get_json()))

    user = UserService.updateUser(current_user_id, request.get_json())
    if (user is None):
        return RouteMaster.not_found_response({'message': 'User not found'})
    return RouteMaster.ok_response({'user': user.to_vo_dict()})

@bp.route('/', methods=['POST'])
@RouteMaster.filter_input
def register_user():
    user = UserService.registerUser(request.get_json())
    RouteMaster.log('Registering user: ' + str(user))

    if (user is None):
        return RouteMaster.error_response({'message': 'User not created'})
    return RouteMaster.created_response({'user': user.to_vo_dict()})

@bp.route('/', methods=['DELETE'])
@jwt_required()
def delete_user():
    user_id = get_jwt_identity()
    user = UserService.getUser(user_id)
    if (user is None):
        return RouteMaster.unauthorized_response({'message': 'User not found'})
        
    current_user_id = get_jwt_identity()
    RouteMaster.log('Deleting user: ' + str(current_user_id))

    user = UserService.deleteUser(current_user_id)
    if (user == True):
        return RouteMaster.ok_response({'message': 'User deleted'})
    return RouteMaster.not_found_response({'message': 'User not deleted'})
