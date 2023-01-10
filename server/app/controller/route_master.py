from functools import wraps
import inspect 
import json
import jsonschema
from jsonschema import validate
import os
from importlib import import_module

from flask import Blueprint, jsonify, request
ROUTES = {}
SANITIZER = {}
CONFIG = {}
LOGGER = None

class UnsafeInputException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class RouteMaster:
    def __init__(self):
        pass

    @staticmethod
    def spawn_routes(config={}, logger=None):
        global CONFIG
        CONFIG = config
        global LOGGER
        LOGGER = logger

        for file in os.listdir(os.path.dirname(os.path.abspath(__file__))):
            if file.endswith(".py") and file != "__init__.py" and file != "route_master.py":
                import_module("app.controller." + file[:-3])

    @staticmethod
    def add_route(route, origins=["*"]):
        frm = inspect.stack()[1]
        mod = inspect.getmodule(frm[0])

        ROUTES[route] = {"name": route, "folder": mod.__name__, "origins": origins, "bp": Blueprint(route, mod.__name__, url_prefix='/'+route)}
        SANITIZER[route] = CONFIG["sanitizer"].get(route, {})
        return ROUTES[route]["bp"]

    @staticmethod
    def filter_input(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            try:
                RouteMaster.sanitize(request)
            except UnsafeInputException as e:
                return RouteMaster.unsafe_input_response("Invalid input")
            except Exception as e:
                return RouteMaster.internal_server_error_response("Sanitizer requested but file missing: " + str(e))
            return f(*args, **kwargs)
        return wrap
    
    @staticmethod
    def log(message):
        if LOGGER is not None:
            LOGGER.info(message)
        else:
            print(message)

    @staticmethod
    def sanitize(request):
        try:
            parts = request.path.split("/")

            sanitizer = SANITIZER
            for part in parts:
                if part == "":
                    continue
                sanitizer = sanitizer[part]
            sanitizer = sanitizer[request.method.lower()]
            if request.data:
                validate(instance=request.get_json(), schema=sanitizer["json"])
            if request.args:
                pargs = {}
                for key, value in request.args.items():
                    if value.isnumeric():
                        pargs[key] = int(value)
                    elif value.lower() == "true":
                        pargs[key] = True
                    elif value.lower() == "false":
                        pargs[key] = False
                    else:
                        pargs[key] = value
                validate(instance=pargs, schema=sanitizer["args"])
        except jsonschema.exceptions.ValidationError as e:
            RouteMaster.log("Schema validation: " + str(e))
            raise UnsafeInputException(e)
        except Exception as e:
            RouteMaster.log("Other exception: " + str(e))
            raise UnsafeInputException(e)
            
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

    @staticmethod
    def forbidden_response(message):
        return jsonify(message), 403

    @staticmethod
    def not_found_response(message):
        return jsonify(message), 404

    @staticmethod
    def created_response(message):
        return jsonify(message), 201

    @staticmethod
    def unsafe_input_response(message):
        return jsonify(message), 422

    @staticmethod
    def internal_server_error_response(message):
        return jsonify(message), 500