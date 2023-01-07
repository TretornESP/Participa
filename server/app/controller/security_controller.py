import os
from .route_master import RouteMaster

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, send_file, current_app
)

bp = RouteMaster.add_route('security', origins = ['*'])

@bp.route('/test', methods=['GET'])
def test():
	return 'Hello World'