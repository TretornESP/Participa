import os
import sys
import json
import logging
import tempfile
import jsonschema
import glob
from jsonschema import validate

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class ServiceLogger(logging.getLoggerClass()):
    def __init__(self, name, level=logging.NOTSET):
        super(ServiceLogger, self).__init__(name, level)
        self.setLevel(level)
        self.buffer = []

    def __call__(self, *args, **kwargs):
        return self

    #Debug level
    def debug(self, msg, *args, **kwargs):
        self.buffer.append(msg)
        super(ServiceLogger, self).debug(msg, *args, **kwargs)

    #Info level
    def info(self, msg, *args, **kwargs):
        self.buffer.append(msg)
        super(ServiceLogger, self).info(msg, *args, **kwargs)
    
    #Warning level
    def warn(self, msg, *args, **kwargs):
        self.buffer.append(msg)
        super(ServiceLogger, self).warn(msg, *args, **kwargs)

    #Error level
    def error(self, msg, *args, **kwargs):
        self.buffer.append(msg)
        super(ServiceLogger, self).error(msg, *args, **kwargs)

    #Critical level
    def critical(self, msg, *args, **kwargs):
        self.buffer.append(msg)
        super(ServiceLogger, self).critical(msg, *args, **kwargs)

    def getLogBuffer(self):
        return self.buffer

class ConfigBase:
    CONF_FOLDER = os.environ.get('CONF_FOLDER', os.getcwd() + '/conf/')

    def __init__(self):
        self.valid = False
        self.data = {}
        print("[CONFIG] Loading configuration from: {}".format(ConfigBase.CONF_FOLDER))
        try:
            for file in os.listdir(ConfigBase.CONF_FOLDER):
                if file.endswith(".json"):
                    print("[CONFIG] Found configuration: {}".format(file))
                    filename = os.path.splitext(file)[0]
                    self.data[filename] = self.__load(os.path.join(ConfigBase.CONF_FOLDER, file))
                    if "$schema" in self.data[filename]:
                        print("[CONFIG] Found schema for configuration: {}".format(file))
                        schema_file = self.data[filename]["$schema"]
                        schema = self.__load(os.path.join(ConfigBase.CONF_FOLDER, schema_file))
                        print("[CONFIG] Validating configuration: {}".format(file))
                        validate(instance=self.data[filename], schema=schema)
                        print("[CONFIG] Validated configuration: {}".format(file))
                    else:
                        print("[CONFIG] No schema found for configuration: {}".format(file))
            
            self.valid = True

        except jsonschema.exceptions.ValidationError as e:
             print("[CONFIG] Error validating configuration: {}".format(e))

        except Exception as e:
            print("[CONFIG] Error loading configuration: {}".format(e))

        logging.basicConfig(
            level=logging.DEBUG,
            stream=sys.stdout,
            filemode="a+",
            format="%(asctime)-15s %(levelname)-8s %(message)s"
        )

        self.log = logging.getLogger("ServiceLogger")
        self.log.info("[CONFIG] Login started")
        self.valid = True

    def __load(self, file):
        try:
            with open(file, 'r') as f:
                return json.load(f)
        except Exception as e:
            raise Exception("[CONFIG] Error loading configuration file: {}, exception: {}".format(file, e))

    def isValid(self):
        return self.valid

    def toDict(self):
        return self.data

class Config(ConfigBase, metaclass=Singleton):
    pass