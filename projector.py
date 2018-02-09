from oscsender import send_osc
from config import basepath, desktoppath, groups
from utils import run_ssh_command
import os, logging


class Projector(object):

    def __init__(self, name, host_ip, position, port,
                 syphon_server=None, app=None, use_checker=None):
        self.host_ip = host_ip
        self.name = name
        self.position = position
        # derive path to corresponding checker app
        self.checker_app = os.path.join(desktoppath,
                                        'checker_%s_%s/checker3.app' % (name, position))
        self.port = port  # osc port of corresponding checker app
        # TODO: maybe do not use the following to attributes here
        self.syphon_server = syphon_server
        self.app = app
        self.use_checker = use_checker
        self.running = False
        self.logger = logging.getLogger(__name__)
    
    def set_config_for_group(self, group):
        try:
            app = groups[group]['projector_settings'][self.name]['app']
            syphon_server = groups[group]['projector_settings'][self.name]['syphon_server']
            use_checker = groups[group]['use_checker']
            self.app = app
            self.syphon_server = syphon_server
            self.use_checker = use_checker
        except KeyError:
            self.logger.warning("Could not find %s's configuration for %s" % (group, self.name))

    def start_checker_app(self):
        self.run_application(self.checker_app)

    def run_application(self, path_to_app, fullscreen=True):
        self.logger.info('Try to run %s on %s (%s)' % (path_to_app, self.host_ip, self.position))
        run_ssh_command('open %s' % path_to_app, self.host_ip)
        if fullscreen:
            cmd = """osascript -e 'tell application \\"System Events\\" to keystroke \\"f\\"'"""
            run_ssh_command(cmd, self.host_ip)
        if self.position == 'right-screen':
            cmd = "osascript %s" % os.path.join(desktoppath, "move_to_right_screen.scpt")
            run_ssh_command(cmd, self.host_ip)

    def set_syphon(self, server, app):
        self.start_checker_app()
        # see https://mutation.gitbooks.io/mutation/content/checker_app.html
        message = '/syphon %s %s' % (server, app)
        send_osc(self.host_ip, self.port, message)
