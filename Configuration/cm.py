import configparser
from gevent import os


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Cm(metaclass=Singleton):
    def __init__(self, configfilename="config.ini"):
        self.config=configparser.ConfigParser()
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.config.read(dir_path+"\\"+configfilename)
