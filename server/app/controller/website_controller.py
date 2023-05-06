import os
import redis
from flask import request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from .route_master import RouteMaster
from app.service.proposal_service import ProposalService
from app.config import Config

bp = RouteMaster.add_route('/', origins = ['https://participasalvaterra.es'])

@bp.route('/', methods=['GET'])
def print_landing_page():
    return "<html><body><h1>Participa Salvaterra</h1></body></html>"