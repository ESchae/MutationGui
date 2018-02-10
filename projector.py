from oscsender import send_osc
from config import basepath, desktoppath, groups
from utils import run_ssh_command
import os, logging, time


class Projector(object):

    def __init__(self, name, host_ip, position, crop):
        self.host_ip = host_ip
        self.name = name
        self.position = position
        self.crop = crop
        # derive path to corresponding checker app
        if self.position == 'right-screen':
            self.checker_app = os.path.join(basepath, 'BetterChecker3000_v2.app')
            self.port = 40100
        else:  # left-screen or main
            self.checker_app = os.path.join(basepath, 'BetterChecker3000_v1.app')
            self.port = 40000
        # the following attributes will be set individually for each group
        self.app = ''
        self.syphon_server = ''
        self.use_checker = None
        self.video = None
        self.logger = logging.getLogger(__name__)
    
    def set_config_for_group(self, group):
        try:
            app = groups[group]['projector_settings'][self.name]['app']
            if app:
                self.app = os.path.join(basepath, group, app)
            else:
                self.app = ''
            self.syphon_server = groups[group]['projector_settings'][self.name]['syphon_server']
            self.use_checker = groups[group]['use_checker']
            self.video = groups[group]['video']
            self.logger.debug('%-12sAPP: %-80s SYPHON: %s USE_CHECKER: %s VIDEO: %-8s ' % (self.name, self.app, self.syphon_server, self.use_checker, self.video))
        except KeyError:
            self.logger.warning("Could not find %s's configuration for %s" % (group, self.name))

    def load(self):
        if not self.use_checker:  # apps that run individually (e.g. MarninTobi)
            self.logger.debug('%s - %s: Starting %s' % (self.host_ip, self.name, self.app))
            self.run_application(self.app)
        elif self.use_checker:
            # start app
            self.logger.debug('%s - %s: Starting %s' % (self.host_ip, self.name, self.app))
            self.run_application(self.app, switch_screen=False)
            # start checker app
            self.logger.debug('%s - %s: Starting %s' % (self.host_ip, self.name, self.checker_app))
            self.run_application(self.checker_app)
            if self.syphon_server:
                if self.position == 'right-screen':
                    port = 40100
                else:
                    port = 40000
                app = os.path.split(self.app)[1].split('.')[0]  # the app name without file extension
                # send syphon server settings to BetterChecker3000
                send_osc(self.host_ip, port, '/checker/syphonServer', [self.syphon_server, app])
            if self.video:
                if self.app:  # do not start on every projector, only the ones specified in config
                    self.logger.debug('%s - %s: Loading %s' % (self.host_ip, self.name, self.app))
                    self.load_video()

    def load_video(self):
        send_osc(self.host_ip, self.port, '/checker/input', [1])
        time.sleep(0.1)
        send_osc(self.host_ip, self.port, '/checker/load', [self.app])
        time.sleep(0.1)
        send_osc(self.host_ip, self.port, '/checker/crop', [self.crop])

    def start_video(self):
        if self.app:
            self.logger.info('%s - %s:\t\t Starting video %s' % (self.host_ip, self.name, self.app))
            send_osc(self.host_ip, self.port, '/checker/play', [])

    def start(self):
        if self.video:
            if self.app:
                self.start_video()

# if video: init-screen = start checker DANN start video
# if not video (aber checker): init-screen = start app + start checker DANN start uber individuelle osc msg
# if not video and not checker: init-screen = start app DANN start uber individuelle osc msg

# globaler RUN button

# load

    def run_application(self, path_to_app, press_keys=['f'], switch_screen=True):
        if not path_to_app:
            return None
        self.logger.info('Try to run %s on %s (%s)' % (path_to_app, self.host_ip, self.position))
        run_ssh_command('open %s' % path_to_app, self.host_ip)
        time.sleep(0.5)
        if self.position == 'right-screen' and switch_screen:
            # switch screen needed only for checker app or app which runs without checker app
            # (not an app which will be send via syphon to checker app)
            cmd = "osascript %s" % os.path.join(basepath, "move_to_right_screen.scpt")
            run_ssh_command(cmd, self.host_ip)
            time.sleep(0.5)
        for key in press_keys:
            cmd = """osascript -e 'tell application \\"System Events\\" to keystroke \\"%s\\"'""" % key
            run_ssh_command(cmd, self.host_ip)
            time.sleep(0.5)

    def quit_application(self, path_to_app):
        self.logger.info('Try to quit %s on %s (%s)' % (path_to_app, self.host_ip, self.position))
        cmd = """osascript -e 'quit app \\"%s\\"'""" % path_to_app
        run_ssh_command(cmd, self.host_ip)
