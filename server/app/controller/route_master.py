from functools import wraps
import inspect 
import os
from importlib import import_module

from flask import Blueprint, jsonify
ROUTES = {}

class RouteMaster:
    def __init__(self):
        pass

    @staticmethod
    def spawn_routes():
        for file in os.listdir(os.path.dirname(os.path.abspath(__file__))):
            if file.endswith(".py") and file != "__init__.py" and file != "route_master.py":
                import_module("app.controller." + file[:-3])

    @staticmethod
    def add_route(route, origins=["*"]):
        frm = inspect.stack()[1]
        mod = inspect.getmodule(frm[0])

        ROUTES[route] = {"name": route, "folder": mod.__name__, "origins": origins, "bp": Blueprint(route, mod.__name__, url_prefix='/'+route)}
        return ROUTES[route]["bp"]

    @staticmethod
    def get_route_for(route):
        return ROUTES[route]
    @staticmethod
    def get_origin_for(route):
        return ROUTES[route]["origins"]
    @staticmethod
    def get_name_for(route):
        return ROUTES[route]["name"]
    @staticmethod
    def get_blueprint_for(route):
        return ROUTES[route]["bp"]
    @staticmethod
    def get_all_routes():
        return ROUTES
    @staticmethod    
    def get_all_names():
        return [ROUTES[route]["name"] for route in ROUTES]
    @staticmethod
    def get_all_origins():
        return [ROUTES[route]["origins"] for route in ROUTES]
    @staticmethod
    def get_all_blueprints():
        return [ROUTES[route]["bp"] for route in ROUTES]

    @staticmethod
    def ok_response(message):
        return jsonify(message), 200
    
    @staticmethod
    def error_response(message):
        return jsonify(message), 400

    @staticmethod
    def auth_required_response(message):
        return jsonify(message), 401