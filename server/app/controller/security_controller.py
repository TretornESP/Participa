import os
from app.model.credentials_model import CredentialsModel
from .route_master import RouteMaster

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, send_file, current_app
)

bp = RouteMaster.add_route('security', origins = ['*'])

@bp.route('/test', methods=['GET'])
def test():
	return 'Hello World'

@bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        user = data['user']
        password = data['password']
        creds = CredentialsModel(user, password)
        