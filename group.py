from config import basepath
import os, configparser


class Group(object):

    def __init__(self, name):
        self.name = name
        self.config = os.path.join(basepath, name, 'config.ini')
        parser = configparser.ConfigParser()
        parser.read(self.config)
