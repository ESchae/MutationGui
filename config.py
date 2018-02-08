import configparser


parser = configparser.ConfigParser()
parser.read('config.ini')

hosts = parser['hosts']
groups = list(parser['groups'].values())
basepath = parser['structure']['basepath']
sudo_password = parser['passwords']['sudo']