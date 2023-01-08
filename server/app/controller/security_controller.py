import os
import redis
from flask import request, current_app
from .route_master import RouteMaster
from app.mapper.user_mapper import UserMapper
from app.service.user_service import UserService

from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity, create_refresh_token, get_jwt
)

bp = RouteMaster.add_route('security', origins = ['*'])

@bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        user = data['username']
        password = data['password']
        creds = CredentialsModel(user, password)

        if (LoginService.login(creds) == True):
            access_token = create_access_token(identity=user)
            refresh_token = create_refresh_token(identity=user)
            return RouteMaster.ok_response(
                {
                    "token": access_token,
                    "refresh": refresh_token,
                    "user": user,
                    "message": "Login successful"
                }
            )
        else:
            return RouteMaster.auth_required_response("Invalid credentials")
    except Exception as e:
        return RouteMaster.error_response("Invalid request")

@bp.route('/validateToken', methods=['GET'])
@jwt_required()
def validate_token():
    current_user_id = get_jwt_identity()
    return RouteMaster.ok_response({"message": "Token is valid", "user": current_user_id})

@bp.route('/refreshToken', methods=['GET'])
@jwt_required(refresh=True)
def refresh_token():
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