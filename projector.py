from oscsender import send_osc
from config import basepath, desktoppath
from utils import run_ssh_command
# from osascript import osascript
import os, logging


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
        self.logger = logging.getLogger(__name__)

    def start_checker_app(self):
        path = os.path.join(desktoppath, self.checker_app, 'checker3.app')
        osa_script_lines = ['tell application \\"%s\\"' % path,
                            'activate',
                            'tell application \\"System Events\\" to keystroke \\"f\\"',
                            'end tell']
        cmd = 'osascript'
        for osa_script_line in osa_script_lines:
            cmd += " -e \'%s\'" % osa_script_line
        self.logger.info(cmd)
        run_ssh_command(cmd, self.host_ip)

    def set_syphon(self, server, app):
        self.start_checker_app()
        # see https://mutation.gitbooks.io/mutation/content/checker_app.html
        message = '/syphon %s %s' % (server, app)
        send_osc(self.host_ip, self.port, message)
