import redis
from datetime import timedelta, datetime, timezone

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from app.config import Config
from app.controller.route_master import RouteMaster

from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity, create_refresh_token, get_jwt
)

def project_init():
    app = Flask(__name__, instance_relative_config=True)

    try:
        cfg = Config()
        app.myconfig = cfg.toDict()
        app.log = cfg.log
        conf = app.myconfig['conf']

        app.jwt = JWTManager(app)
        app.jwt_redis_blocklist = redis.StrictRedis(
            host=app.myconfig["conf"]["trashcan_hostname"],
            port=app.myconfig["conf"]["trashcan_port"],
            db=app.myconfig["conf"]["trashcan_db"],
            password=app.myconfig["conf"]["trashcan_password"],
            decode_responses=True
        )

        @app.jwt.token_in_blocklist_loader
        def check_if_token_in_blocklist(jwt_header, jwt_payload: dict):
            jti = jwt_payload['jti']
            token_in_blocklist = app.jwt_redis_blocklist.get(jti)
            return token_in_blocklist is not None

        @app.after_request
        def refresh_expiring_jwts(response):
            try:
                exp_timestamp = get_jwt()["exp"]
                now = datetime.now(timezone.utc)
                target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
                if target_timestamp > exp_timestamp:
                    access_token = create_access_token(identity=get_jwt_identity())
                    set_access_cookies(response, access_token)
                return response
            except (RuntimeError, KeyError):
                # Case where there is not a valid JWT. Just return the original response
                return response

        
    except KeyError:
        app.log.error("[INIT] Configuration not found!")
        return None
    except Exception as e:
        print("[INIT] Error loading configuration: {}".format(e))
        return None

    try:
        app.config["APPLICATION_ROOT"] = conf['api_root']
        app.config["JWT_SECRET_KEY"] = conf['secret_key']
        app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=conf['access_token_expiration'])
        app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=conf['refresh_token_expiration'])
        
        with app.app_context():
            app.log.info("[INIT] Registering routes...")
            resources = {}
            blueprints = []
            RouteMaster.spawn_routes()

            for route in RouteMaster.get_all_routes():
                app.log.info("[INIT] Registering router: " + RouteMaster.get_name_for(route))
                blueprints.append(RouteMaster.get_blueprint_for(route))
                resources["/{}/*".format(RouteMaster.get_name_for(route))] = {"origins": RouteMaster.get_origin_for(route)}
            
            if (conf['cors'] == True):
                app.log.info("[INIT] CORS enabled, resources: " + str(resources))
                CORS(app, resources=resources)
            else:
                app.log.warn("[INIT] CORS disabled")

            for blueprint in blueprints:
                app.register_blueprint(blueprint)
        
            return app
    except Exception as e:
        app.log.error("[INIT] Error starting application: {}".format(e))
        return None