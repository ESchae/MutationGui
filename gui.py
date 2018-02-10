import Tkinter as tk
import tkMessageBox
from config import hosts, groups, basepath
from host import Host
from projector import Projector
import logging, os, time
from datetime import datetime
from utils import run_shell_command, run_ssh_command
from oscsender import send_osc

logging.basicConfig(level=logging.DEBUG)


class ProjectorFrame(tk.Frame):

    def __init__(self, parent, projector, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.projector = projector

        self.info = tk.LabelFrame(self, text='Projector: %s' % projector.name)
        self.position = tk.Label(self.info, text='Position: %s' % self.projector.position)
        app_name = os.path.split(self.projector.app)[1]
        self.app = tk.Label(self.info, text='App: %s' % app_name)

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
        app_name = os.path.split(self.projector.app)[1]
        self.app['text'] = 'App: %s' % app_name


class HostFrame(tk.Frame):

    def __init__(self, parent, host, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.host = host

        label_text = 'Mutation %s %s' % (host.number, host.ip_address)
        self.label = tk.Label(self, text=label_text)
        self.shutdown_button = tk.Button(self, text='Shutdown [Not working]', command=host.shutdown)
        self.restart_button = tk.Button(self, text='Restart [Not working]', command=host.restart)
        self.screenshare_button = tk.Button(self, text='Open Screenshare', command=host.open_screensharing)
        self.conection_label = tk.Label(self, text='')

        self.label.pack(side='top', fill='x', expand=True)
        self.shutdown_button.pack(side='bottom', fill='both', expand=True)
        self.restart_button.pack(side='bottom', fill='both', expand=True)
        self.screenshare_button.pack(side='bottom', fill='both', expand=True)
        self.conection_label.pack(side='top', fill='both', expand=True)

    def set_connection(self):
        time = datetime.now().time().replace(microsecond=0)
        if self.host.reachable():
            text = 'Reachable\n(last checked: %s)' % time
            color = 'green'
        else:
            text = 'Unrechable\n(last checked: %s)' % time
            color = 'red'
        self.conection_label['text'] = text
        self.conection_label['fg'] = color
        # self.parent.after(5000, self.check_connection)


class MutationGui(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.logger = logging.getLogger(__name__)
        self.parent = parent
        self.parent.title('Mutation')

        self.main_window = tk.Frame(parent)
        self.main_window.pack(side="top", fill="both", expand=True)

        self.main_control_panel = tk.Frame(self.main_window)
        self.hosts_control_panel = tk.Frame(self.main_window)
        self.main_control_panel.pack(side='top', fill='x', expand=False)
        self.hosts_control_panel.pack(side='top', fill='both', expand=False)

        self.group_label = tk.Label(self.main_control_panel, text='Select group: ')
        self.selected_group = tk.StringVar(self.main_control_panel)
        self.selected_group.trace('w', self.change_group)
        self.group = tk.OptionMenu(self.main_control_panel, self.selected_group, *groups)
        self.update_button = tk.Button(self.main_control_panel, text='Update Files on Hosts', command=self.update)
        self.check_connection_button = tk.Button(self.main_control_panel, text='Check connections', command=self.check_connections)
        self.load_button = tk.Button(self.main_control_panel, text='Open Apps', command=self.load)
        self.start_button = tk.Button(self.main_control_panel, text='Play App', command=self.start, state='disabled')
        self.quit_apps_button = tk.Button(self.main_control_panel, text='Quit All Apps', command=self.quit_apps)

        self.group_label.pack(side='left', expand=True)
        self.group.pack(side='left', fill='x', expand=True)
        self.update_button.pack(side='left', expand=True)
        self.check_connection_button.pack(side='left', expand=True)
        self.load_button.pack(side='left', expand=True)
        self.start_button.pack(side='left', expand=True)
        self.quit_apps_button.pack(side='left', expand=True)

        self.host_frames = []
        self.projector_frames = []

        for host_number in hosts:
            ip_address = hosts[host_number]['ip_address']
            host = Host(host_number, ip_address)
            host_frame = HostFrame(self.hosts_control_panel, host)
            host_frame.pack(side='left', fill='both', expand=True)
            self.host_frames.append(host_frame)
            for projector in sorted(hosts[host_number]['projectors']):
                projector = hosts[host_number]['projectors'][projector]
                p = Projector(projector['name'], ip_address, projector['position'], projector['crop'])
                projector_frame = ProjectorFrame(host_frame, p)
                projector_frame.pack(side='right', fill='both', expand=True)
                self.projector_frames.append(projector_frame)

        self.selected_group.set('TeamTest')
        self.check_connections()

    def change_group(self, *args):
        self.start_button['state'] = 'disabled'
        group = self.selected_group.get()
        self.logger.info('Changed group to %s' % group)
        self.update_projector_frames()

    def update_projector_frames(self):
        for projector_frame in self.projector_frames:
            projector_frame.update_labels(self.selected_group.get())

    def check_connections(self):
        for host in self.host_frames:
            host.set_connection()

    def load(self):
        if tkMessageBox.askyesno('', 'Selected group: %s - Correct?' % self.selected_group.get()):
            for projector_frame in self.projector_frames:
                projector_frame.projector.load()
            self.start_button['state'] = 'normal'

    def start(self):
        for projector_frame in self.projector_frames:
            projector_frame.projector.start()
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
        for host_frame in self.host_frames:
            host_frame.host.quit_any_apps()

    def start_checker_apps(self):
        for projector_frame in self.projector_frames:
            projector_frame.start_checker_app()

    def update(self):
        """ Update the foulder given in config.py as basepath on
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
            self.logger.debug('UPDATE: Using rsync for other groups')
            source = basepath
            destination = basepath[:-1]
            cmd = 'prsync -r -v -H "%s" %s %s' % (' '.join(host_ips), source, destination)
            run_shell_command(cmd)
        self.logger.info('Updated %s on all hosts (%s)' % (source, host_ips))

    def start_video(self):
        for projector_frame in self.projector_frames:
            projector_frame.projector.start_video()


if __name__ == "__main__":
    root = tk.Tk()
    MutationGui(root)
    root.mainloop()
