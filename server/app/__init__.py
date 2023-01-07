from flask import Flask
from flask_cors import CORS
from app.config import Config
from app.controller.route_master import RouteMaster

def project_init():
    app = Flask(__name__, instance_relative_config=True)

    try:
        cfg = Config()
        app.myconfig = cfg.toDict()
        app.log = cfg.log
        conf = app.myconfig['conf']
    except KeyError:
        app.log.error("[INIT] Configuration not found!")
        return None
    except Exception as e:
        print("[INIT] Error loading configuration: {}".format(e))
        return None

    try:
        app.config["APPLICATION_ROOT"] = conf['api_root']
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