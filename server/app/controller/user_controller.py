import os
import redis
from flask import request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity

from .route_master import RouteMaster
from app.mapper.user_mapper import UserMapper
from app.service.user_service import UserService



bp = RouteMaster.add_route('user', origins = ['*'])

@bp.route('/', methods=['GET'])
@jwt_required()
def get_user():
     current_user_id = get_jwt_identity()
     user = UserService.getUser(current_user_id)
     if (user is None):
         return RouteMaster.not_found_response({'message': 'User not found'})
     return RouteMaster.ok_response({'user': user.to_vo_dict()})

@bp.route('/', methods=['PUT'])
@jwt_required()
def update_user():
    current_user_id = get_jwt_identity()
    user = UserService.updateUser(current_user_id, request.get_json())
    if (user is None):
        return RouteMaster.not_found_response({'message': 'User not found'})
    return RouteMaster.ok_response({'user': user.to_vo_dict()})