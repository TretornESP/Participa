import os
import redis

from app.model.credentials_model import CredentialsModel
from app.mapper.user_mapper import UserMapper
from app.service.login_service import LoginService
from .route_master import RouteMaster

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, send_file, current_app
)

from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity, create_refresh_token, get_jwt
)

bp = RouteMaster.add_route('security', origins = ['*'])
config = current_app.myconfig['conf']
jwt = current_app.jwt

jwt_redis_blocklist = redis.StrictRedis(
    host=config["trashcan_hostname"],
    port=config["trashcan_port"],
    db=config["trashcan_db"],
    password=config["trashcan_password"],
    decode_responses=True
)


@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload: dict):
    jti = jwt_payload['jti']
    token_in_blocklist = jwt_redis_blocklist.get(jti)
    return token_in_blocklist is not None


@bp.route('/test', methods=['GET'])
def test():
	return 'Hello World'

@bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        user = data['username']
        password = data['password']
        creds = CredentialsModel(user, password)

        if LoginService.login(creds):
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

@bp.route('/listUsers', methods=['GET'])
def list_users():
    return {"users": UserMapper.model_to_dict_list(LoginService.list_users())}, 200

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
        jwt_redis_blocklist.set(jti, '', ex=current_app.config['JWT_ACCESS_TOKEN_EXPIRES'] * 3600)
    else:
        jwt_redis_blocklist.set(jti, '', ex=current_app.config['JWT_REFRESH_TOKEN_EXPIRES'] * (24*3600))
        
    return RouteMaster.ok_response({"msg":f"{ttype.capitalize()} token successfully revoked"})