from oscsender import send_osc
from config import basepath
# from osascript import osascript
import os


class Projector(object):

    def __init__(self, name, host_ip, position, checker_app, port,
                 syphon_server=None, app=None):
        self.host_ip = host_ip
        self.name = name
        self.position = position
        self.checker_app = checker_app  # name of corresponding checker app
        self.port = port  # osc port of corresponding checker app
        self.syphon_server = syphon_server
        self.app = app
        self.running = False

    def start_checker_app(self):
        path = os.path.join(basepath, self.checker_app)
        osa_script = 'tell application "%s" to activate'
        #returncode, stdout, stderr = osascript(osa_script)
        #return returncode, stdout, stderr

    def set_syphon(self, server, app):
        self.start_checker_app()
        # see https://mutation.gitbooks.io/mutation/content/checker_app.html
        message = '/syphon %s %s' % (server, app)
        send_osc(self.host_ip, self.port, message)