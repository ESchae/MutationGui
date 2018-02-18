import Tkinter as tk
import tkMessageBox
import logging
import os
from config import hosts, groups, basepath
from host import Host
from projector import Projector
from datetime import datetime
from utils import run_shell_command
from oscsender import send_osc


class ProjectorFrame(tk.Frame):
    """ Info panel used for each projector.

    Displays information on projector name, position and app.
    The app depends on the currently selected group.

    """

    def __init__(self, parent, projector, *args, **kwargs):
        """ Initialise the projector info panel frame.

        :param parent: Parent frame, in which ProjectorFrame should be drawn.
        :param projector: Projector for which info should be displayed.
        :param args: Any remaining optional arguments for a Tkinter Frame.
        :param kwargs: Any remaining optional keyword args for a Tkinter Frame.
        """
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.projector = projector

        # the frame elements
        self.info = tk.LabelFrame(
            self, text='Projector: %s' % projector.name)
        self.position = tk.Label(
            self.info, text='Position: %s' % self.projector.position)
        self.app = tk.Label(
            self.info, text='App: %s' % self.projector.app_short_name)

        # arrange the frame elements
        self.position.pack(side='top', fill='x', expand=True)
        self.app.pack(side='top', fill='both', expand=True)
        self.info.pack(side='top', fill='both', expand=True)

    def start_checker_app(self):
        self.projector.run_application(self.projector.checker_app)

    def quit_checker_app(self):
        self.projector.quit_application(self.projector.checker_app)

    def quit_app(self):
        path = self.projector.app
        self.projector.quit_application(path)
    
    def send_syphon(self):
        self.projector.send_syphon()

    def update_labels(self, current_group):
        self.projector.set_config_for_group(current_group)
        self.app['text'] = 'App: %s' % self.projector.app_short_name


class HostFrame(tk.Frame):
    """ Info panel used for each host.

    Displays information on host number, ip address, whether the host is
    reachable via ssh, the connected projectors and three buttons to open
    screenshare, restart and shutdown the host.

    """

    def __init__(self, parent, host, *args, **kwargs):
        """ Initialise the host info panel frame.

        :param parent: Parent frame, in which HostFrame should be drawn.
        :param host: Host for which info should be displayed.
        :param args: Any remaining optional arguments for a Tkinter Frame.
        :param kwargs: Any remaining optional keyword args for a Tkinter Frame.
        """
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.host = host

        # the frame elements
        self.label = tk.Label(
            self, text='Mutation %s %s' % (host.number, host.ip_address))
        self.shutdown_button = tk.Button(
            self, text='Shutdown [Not working]', command=host.shutdown)
        self.restart_button = tk.Button(
            self, text='Restart [Not working]', command=host.restart)
        self.screenshare_button = tk.Button(
            self, text='Open Screenshare', command=host.open_screensharing)
        self.connection_label = tk.Label(self, text='')

        # arrange the frame elements
        self.label.pack(side='top', fill='x', expand=True)
        self.shutdown_button.pack(side='bottom', fill='both', expand=True)
        self.restart_button.pack(side='bottom', fill='both', expand=True)
        self.screenshare_button.pack(side='bottom', fill='both', expand=True)
        self.connection_label.pack(side='top', fill='both', expand=True)

    def check_connection(self):
        time = datetime.now().time().replace(microsecond=0)
        if self.host.reachable():
            text = 'Reachable\n(last checked: %s)' % time
            color = 'green'
        else:
            text = 'Unrechable\n(last checked: %s)' % time
            color = 'red'
        self.connection_label['text'] = text
        self.connection_label['fg'] = color


class MutationGui(tk.Frame):
    """
    Main frame of the Gui.

    Displays all hosts as HostFrame together with their corresponding
    projectors as ProjectorFrame.
    Moreover includes group selection and buttons for updating the files,
    check connections, open apps, play apps and quit all apps.

    """

    def __init__(self, parent, *args, **kwargs):
        """ Initialise the main mutation gui frame.

        :param parent: Parent frame, in which HostFrame should be drawn.
        :param args: Any remaining optional arguments for a Tkinter Frame.
        :param kwargs: Any remaining optional keyword args for a Tkinter Frame.
        """
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.logger = logging.getLogger(__name__)
        self.parent = parent
        self.parent.title('Mutation')

        # main frame which contains all other frames
        self.main_window = tk.Frame(parent)
        self.main_window.pack(side="top", fill="both", expand=True)

        # main control panel with group selection and global buttons
        self.main_control_panel = tk.Frame(self.main_window)
        self.hosts_control_panel = tk.Frame(self.main_window)
        self.main_control_panel.pack(side='top', fill='x', expand=False)
        self.hosts_control_panel.pack(side='top', fill='both', expand=False)
        # group selection
        self.group_label = tk.Label(
            self.main_control_panel, text='Select group: ')
        self.selected_group = tk.StringVar(self.main_control_panel)
        self.selected_group.trace('w', self.change_group)
        self.group = tk.OptionMenu(
            self.main_control_panel, self.selected_group, *groups)
        # global buttons
        self.update_button = tk.Button(
            self.main_control_panel,
            text='Update Files on Hosts',
            command=self.update)
        self.check_connection_button = tk.Button(
            self.main_control_panel,
            text='Check connections',
            command=self.check_connections)
        self.open_apps_button = tk.Button(
            self.main_control_panel,
            text='Open Apps',
            command=self.open_apps)
        self.play_apps_button = tk.Button(
            self.main_control_panel,
            text='Play Apps',
            command=self.play_apps,
            state='disabled')
        self.quit_apps_button = tk.Button(
            self.main_control_panel,
            text='Quit All Apps',
            command=self.quit_apps)

        # arrange the frame elements of main control panel
        self.group_label.pack(side='left', expand=True)
        self.group.pack(side='left', fill='x', expand=True)
        self.update_button.pack(side='left', expand=True)
        self.check_connection_button.pack(side='left', expand=True)
        self.open_apps_button.pack(side='left', expand=True)
        self.play_apps_button.pack(side='left', expand=True)
        self.quit_apps_button.pack(side='left', expand=True)

        # initialise host and corresponding projector frames
        self.host_frames = []
        self.projector_frames = []
        for host_number in hosts:
            ip_address = hosts[host_number]['ip_address']
            host = Host(host_number, ip_address)
            host_frame = HostFrame(self.hosts_control_panel, host)
            host_frame.pack(side='left', fill='both', expand=True)
            self.host_frames.append(host_frame)
            for projector_num in sorted(hosts[host_number]['projectors']):
                projector_info = hosts[host_number]['projectors'][projector_num]
                projector = Projector(projector_info['name'],
                                      ip_address,
                                      projector_info['position'],
                                      projector_info['crop'])
                projector_frame = ProjectorFrame(host_frame, projector)
                projector_frame.pack(side='right', fill='both', expand=True)
                self.projector_frames.append(projector_frame)

        self.selected_group.set('TeamTest')
        self.check_connections()

    def change_group(self, *args):
        self.play_apps_button['state'] = 'disabled'  # app must be opened first
        group = self.selected_group.get()
        self.logger.info('Changed group to %s' % group)
        self.update_projector_frames()

    def update_projector_frames(self):
        for projector_frame in self.projector_frames:
            projector_frame.update_labels(self.selected_group.get())

    def check_connections(self):
        for host in self.host_frames:
            host.check_connection()

    def open_apps(self):
        question = 'Selected group: %s - Correct?' % self.selected_group.get()
        if tkMessageBox.askyesno('', question):
            for projector_frame in self.projector_frames:
                projector_frame.projector.open_app()
            self.play_apps_button['state'] = 'normal'

    def play_apps(self):
        for projector_frame in self.projector_frames:
            projector_frame.projector.play_app()
        # start sound and other group specific things via osc
        # those things need to be set in a seperate supercollider script
        # or something similar
        group = self.selected_group.get()
        osc_msg = '/mutation/start/%s' % group
        send_osc("127.0.0.1", 57120, osc_msg, [])

    def send_syphon(self):
        self.logger.info('Sending syphon info to all projectors')
        for projector_frame in self.projector_frames:
            projector_frame.send_syphon()
    
    def start_apps(self):
        for projector_frame in self.projector_frames:
            projector_frame.start_app()

    def quit_apps(self):
        # stop sound
        group = self.selected_group.get()
        osc_msg = '/mutation/stop/%s' % group
        send_osc("127.0.0.1", 57120, osc_msg, [])
        # will repeat cmd+q four times on every host
        # TODO: Close specific opened apps on projectors
        # Note: Actually the only opened apps should be for each projector
        # the checker_app and app - should be easy to close them directly
        for host_frame in self.host_frames:
            host_frame.host.quit_any_apps()

    def start_checker_apps(self):
        for projector_frame in self.projector_frames:
            projector_frame.start_checker_app()

    def update(self):
        """
        Update the folder given in config.py as basepath on
        all hosts using rsync. This will only update files
        that have changed. Files that lie only on hosts
        will not be deleted.
        """
        current_group = self.selected_group.get()
        host_ips = [hosts[host]['ip_address'] for host in hosts]
        if current_group == 'Tim':
            # this is a quick (and not so nice) fix
            # tim's app could not be opened via ssh after using prsync
            # though it could be opened manually on every host
            # the problem did not happen while using scp, hence for tim
            # scp is used
            # if someone has more time in the future and runs in a similar
            # problem, it could be beneficial to debug in more detail
            self.logger.debug('UPDATE: Using scp for Tim')
            source = os.path.join(basepath, current_group) + '/'
            destination = basepath
            for host_ip in host_ips:
                # could be tried using pscp
                cmd = 'scp -r %s %s:%s' % (source, host_ip, destination)
                run_shell_command(cmd)
        else:
            self.logger.debug('UPDATE: Using rsync for group which is not Tim')
            source = basepath
            destination = basepath[:-1]
            cmd = 'prsync -r -v -H "%s" %s %s' \
                  % (' '.join(host_ips), source, destination)
            run_shell_command(cmd)
        self.logger.info('Updated %s on all hosts (%s)' % (source, host_ips))

    def start_video(self):
        for projector_frame in self.projector_frames:
            projector_frame.projector.start_video()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description='Gui for Mutation project at IMWI (MUT) Karlsruhe.'
    )
    parser.add_argument(
        '-v', '--verbose', help='Increase log output verbosity',
        action='store_true'
    )
    args = parser.parse_args()

    # set log output verbosity
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    # start main drawing loop
    root = tk.Tk()
    MutationGui(root)
    root.mainloop()
