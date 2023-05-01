import os
import redis
from flask import request, current_app
from .route_master import RouteMaster, UnsafeInputException

from app.service.login_service import LoginService
from app.service.user_service import UserService

from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity, create_refresh_token, get_jwt
)

bp = RouteMaster.add_route('security', origins = ['*'])

@bp.route('/login', methods=['POST'])
@jwt_required(optional=True)
@RouteMaster.filter_input
def login():

    data = request.get_json()
    user = data['username']
    password = data['password']
    
    current_identity = get_jwt_identity()
    if (current_identity is not None):
        return RouteMaster.ok_response({"message": "Already logged in"})

    try:
        if (LoginService.login(user, password) != True):
            raise UnsafeInputException("Invalid credentials")

        user_model = UserService.getUserByEmail(user)
        if (user_model is None):
            raise UnsafeInputException("Invalid credentials")
        
        if (user_model.get_deleted_at() != 0):
            raise UnsafeInputException("User is deleted")

        access_token = create_access_token(identity=user_model.get_uid())
        refresh_token = create_refresh_token(identity=user_model.get_uid())

        return RouteMaster.ok_response(
            {
                "token": access_token,
                "refresh": refresh_token,
                "user": user_model.to_vo_dict(),
                "message": "Login successful"
            }
        )
    except UnsafeInputException as e:
        return RouteMaster.auth_required_response("Invalid credentials")
    except Exception as e:
        RouteMaster.log(e)
        return RouteMaster.error_response(str(e))

@bp.route('/validateToken', methods=['GET'])
@jwt_required()
def validate_token():
    current_user_id = get_jwt_identity()
    user_id = get_jwt_identity()
    user = UserService.getUser(user_id)
    if (user is None):
        return RouteMaster.ok_response({"message": "Token is valid but user doesnt exist!", "user": current_user_id})

    return RouteMaster.ok_response({"message": "Token is valid", "user": current_user_id})

@bp.route('/refreshToken', methods=['GET'])
@jwt_required(refresh=True)
def refresh_token():
    current_user_id = get_jwt_identity()
    user_id = get_jwt_identity()
    user = UserService.getUser(user_id)
    if (user is None):
        return RouteMaster.unauthorized_response({"message": "Cant refresh token, user doesnt exist!"})

    current_user_id = get_jwt_identity()
    access_token = create_access_token(identity=current_user_id)
    return RouteMaster.ok_response({"token": access_token, "user": current_user_id, "message": "Token refreshed"})

@bp.route('/logout', methods=['DELETE'])
@jwt_required(verify_type=False)
def logout():
    jti = get_jwt()['jti']
    ttype = get_jwt()['type']

    if ttype == 'access':
        current_app.jwt_redis_blocklist.set(jti, '', ex=current_app.config['JWT_ACCESS_TOKEN_EXPIRES'] * 3600)
    else:
        current_app.jwt_redis_blocklist.set(jti, '', ex=current_app.config['JWT_REFRESH_TOKEN_EXPIRES'] * (24*3600))
        
    return RouteMaster.ok_response({"msg":f"{ttype.capitalize()} token successfully revoked"})