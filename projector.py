""" Module with functionality corresponding to projectors.

Copyright 2018
Author Elke Schaechtele <elke.schaechtele@stud.hfm-karlsruhe.de>
"""
import os
import logging
import time
from oscsender import send_osc
from config import basepath, desktoppath, groups
from bash import run_ssh_command


class Projector(object):

    def __init__(self, name, host_ip, position, crop):
        """ Initialisation of a projector.

        For detailed notes on parameters please also refer to config.py.

        :param (str) name: The name of the projector.
        :param (str) host_ip: The ip address of the corresponding host.
        :param (str) position: right-screen, left-screen or main
        :param (float) crop: Value used for crop of projection screen.
        """
        # global attributes
        self.host_ip = host_ip
        self.name = name
        self.position = position
        self.crop = crop
        self.logger = logging.getLogger(__name__)

        # derive path to corresponding checker app and port
        if self.position == 'right-screen':
            checker_app = 'BetterChecker3000_v2.app'
            self.port = 40100
        else:  # left-screen or main
            checker_app = 'BetterChecker3000_v1.app'
            self.port = 40000
        self.checker_app = os.path.join(desktoppath, checker_app)

        # the following attributes will be set individually for each group
        self.app = ''
        self.app_short_name = ''
        self.syphon_server = ''
        self.use_checker = None
        self.video = None
    
    def set_config_for_group(self, group):
        """ Set app, syphon_server and video settings for given group.

        :param (str) group: Name of selected group. Must be one from config.py
        :return: None
        """
        group_settings = groups[group]['projector_settings'][self.name]
        try:
            app = group_settings['app']
            if app:
                self.app = os.path.join(basepath, group, app)
                self.app_short_name = os.path.split(self.app)[1]
            else:
                self.app = ''
            self.syphon_server = group_settings['syphon_server']
            self.use_checker = groups[group]['use_checker']
            self.video = groups[group]['video']
            self.logger.debug(
                '%-12sAPP: %-80s SYPHON: %s USE_CHECKER: %s VIDEO: %-8s '
                % (self.name, self.app, self.syphon_server,
                   self.use_checker, self.video))
        except KeyError:
            self.logger.warning(
                "Could not find %s's configuration for %s"
                % (group, self.name))

    def open_app(self):
        """ Open app for this projector.

        Depending on the group settings, different scenarios are possible.
        In 2018 the following scenarios were present:

        MarninTobi had a app, that made the mapping itself without the
        BetterChecker3000 App. Once the app was opened in full screen on every
        projector, it only had to be started via osc.

        All other groups were dependent on the mapping of the BetterChecker3000
        App. Alessandro and Tim had an app, which needed to be opened first.
        Then the BetterChecker3000 App was opened in full screen on every
        projector, ready to display the app via syphon.
        Both apps could then be started (and closed) via osc. The osc messages
        were send via the Play Apps button of the main gui and corresponding
        actions implemented in a separate supercollider file.

        Vanessa had a video file. First the video was opened (actually this
        could be also left out), then the BetterChecker3000 App like above.
        To start the video, osc messaged (see start_video) were sent to
        the BetterCheckerApp3000 after the Play Apps button of the main gui
        was pressed.

        """
        if not self.app:  # only start if app was specified in config
            return None
        if not self.use_checker:  # apps that run individually, e.g. MarninTobi
            self.logger.debug(
                '%s - %s: Starting %s' % (self.host_ip, self.name, self.app))
            self.run_application(self.app)
        else:
            # start app
            self.logger.debug(
                '%s - %s: Starting %s' % (self.host_ip, self.name, self.app))
            # do not move the window to the second screen here, because then
            # the focus will be on the wrong screen when the checker app
            # will be opened
            self.run_application(self.app, switch_screen=False)
            # start checker app
            self.logger.debug(
                '%s - %s: Starting %s' % (self.host_ip, self.name,
                                          self.checker_app))
            self.run_application(self.checker_app)
            if self.syphon_server:
                self.send_syphon()
            if self.video:
                self.load_video()

    def send_syphon(self):
        """ Send syphon server settings to BetterChecker3000 via osc. """
        app = self.app_short_name.split('.')[0]  # app without file extension
        send_osc(self.host_ip, self.port, '/checker/syphonServer',
                 [self.syphon_server, app])

    def load_video(self):
        self.logger.debug(
            '%s - %s: Loading %s' % (self.host_ip, self.name, self.app))
        send_osc(self.host_ip, self.port, '/checker/input', [1])
        time.sleep(0.1)
        send_osc(self.host_ip, self.port, '/checker/load', [self.app])
        time.sleep(0.1)
        send_osc(self.host_ip, self.port, '/checker/crop', [self.crop])

    def start_video(self):
        self.logger.info(
            '%s - %s:\t\t Starting video %s'
            % (self.host_ip, self.name, self.app))
        send_osc(self.host_ip, self.port, '/checker/play', [])

    def play_app(self):
        if not self.app:  # only start if app was specified in config
            return None
        if self.video:
            self.start_video()
        # TODO: Here start possibilities for other groups could be implemented
        # see docstring of method open_apps()

    def run_application(self, path_to_app, press_keys=['f'], switch_screen=True):
        if not path_to_app:
            return None
        self.logger.info(
            'Try to run %s on %s (%s)'
            % (path_to_app, self.host_ip, self.position))
        run_ssh_command('open %s' % path_to_app, self.host_ip)
        time.sleep(0.5)
        if self.position == 'right-screen' and switch_screen:
            # switch screen needed only for BetterChecker3000 App
            # or app which runs without checker app --> apps that need to be
            # run in full screen on every projector;
            # not an app which will be send via syphon to checker app
            cmd = "osascript %s" % os.path.join(basepath,
                                                "move_to_right_screen.scpt")
            run_ssh_command(cmd, self.host_ip)
            time.sleep(0.5)
        for key in press_keys:
            cmd = """osascript -e 'tell application \\"System Events\\" to keystroke \\"%s\\"'""" % key
            run_ssh_command(cmd, self.host_ip)
            time.sleep(0.5)

    def quit_app(self, path_to_app):
        # TODO: quit app and checker_app if self.user_checker is True
        self.logger.info(
            'Try to quit %s on %s (%s)'
            % (path_to_app, self.host_ip, self.position))
        cmd = """osascript -e 'quit app \\"%s\\"'""" % path_to_app
        run_ssh_command(cmd, self.host_ip)
