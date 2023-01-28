import os
import redis
from flask import request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity

from .route_master import RouteMaster
from app.service.uploads_service import UploadsService


bp = RouteMaster.add_route('uploads', origins = ['*'])

@bp.route('/photo', methods=['POST'])
@jwt_required()
def upload_photo():
    current_user_id = get_jwt_identity()
    if 'file' not in request.files:
        return RouteMaster.error_response({'message': 'No file part'})
    
    file = request.files['file']

    if file.filename == '':
        return RouteMaster.error_response({'message': 'No selected file'})

    if file:
        filename = UploadsService.upload_photo(file, current_user_id)
        if filename is None:
            return RouteMaster.error_response({'message': 'File not saved'})
        return RouteMaster.created_response({'id': filename})