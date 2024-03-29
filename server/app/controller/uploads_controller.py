import os
import redis
from flask import request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity

from .route_master import RouteMaster
from app.service.uploads_service import UploadsService
from app.config import Config

bp = RouteMaster.add_route('uploads', origins = ['https://participasalvaterra.es'])

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
        
        
        method = Config().toDict()['conf']['method']
        hostname = Config().toDict()['conf']['hostname']
        port = Config().toDict()['conf']['port']

        return RouteMaster.created_response({'url': filename})

@bp.route('/photo/<folder>/<image>', methods=['GET'])
@jwt_required()
def get_photo(folder, image):
    current_user_id = get_jwt_identity()
    url = UploadsService.presign(folder+"/"+image)
    if url is None:
        return RouteMaster.error_response({'message': 'File not found'})
    return RouteMaster.ok_response({'url': url})