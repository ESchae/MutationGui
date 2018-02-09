import Tkinter as tk
from config import hosts, groups, basepath
from host import Host
from projector import Projector
import logging, os, time
from datetime import datetime
from utils import run_shell_command, run_ssh_command

logging.basicConfig(level=logging.DEBUG)


class ProjectorFrame(tk.Frame):

    def __init__(self, parent, projector, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.projector = projector

        self.info = tk.LabelFrame(self, text='Projector: %s' % projector.name)
        #self.host_ip = tk.Label(self.info, text='Host: %s' % self.projector.host_ip)
        self.position = tk.Label(self.info, text='Position: %s' % self.projector.position)
        self.port = tk.Label(self.info, text='Checker Port: %s' % self.projector.port)
        self.syphon_server = tk.Label(self.info, text='Syphon: %s' % self.projector.syphon_server)
        app_name = os.path.split(self.projector.app)[1]
        self.app = tk.Label(self.info, text='App: %s' % app_name)
        # self.use_checker = tk.Label(self.info, text='Use checker: %s' % self.projector.use_checker)

        #self.host_ip.pack(side='top', fill='x', expand=True)
        self.position.pack(side='top', fill='x', expand=True)
        self.port.pack(side='top', fill='both', expand=True)
        self.syphon_server.pack(side='top', fill='both', expand=True)
        self.app.pack(side='top', fill='both', expand=True)
        self.info.pack(side='top', fill='both', expand=True)
        # self.use_checker.pack(side='top', fill='both', expand=True)

    def start_checker_app(self):
        self.projector.run_application(self.projector.checker_app, press_keys=['f', 'g'])

    def quit_checker_app(self):
        self.projector.quit_application(self.projector.checker_app)
    
    def start_app(self):
        path = self.projector.app
        self.projector.run_application(path)

    def quit_app(self):
        path = self.projector.app
        self.projector.quit_application(path)

    def update_labels(self, current_group):
        self.projector.set_config_for_group(current_group)
        app_name = os.path.split(self.projector.app)[1]
        self.app['text'] = 'App: %s' % app_name
        self.syphon_server['text'] = 'Syphon: %s' % self.projector.syphon_server
        # self.use_checker['text'] = 'Use checker: %s' % self.projector.use_checker


class HostFrame(tk.Frame):

    def __init__(self, parent, host, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.host = host

        label_text = 'Mutation %s %s' % (host.number, host.ip_address)
        self.label = tk.Label(self, text=label_text)
        self.shutdown_button = tk.Button(self, text='Shutdown', command=host.shutdown)
        self.restart_button = tk.Button(self, text='Restart', command=host.restart)
        self.screenshare_button = tk.Button(self, text='Open Screenshare', command=host.open_screensharing)
        #self.files = tk.Listbox(self)
        #self.files_label = tk.Label(self, text='Files at ')

        # show connection info
        self.conection_label = tk.Label(self, text='')

        self.label.pack(side='top', fill='x', expand=True)
        #self.files_label.pack(side='top', fill='x', expand=True)
        #self.files.pack(side='left')
        self.shutdown_button.pack(side='bottom', fill='both', expand=True)
        self.restart_button.pack(side='bottom', fill='both', expand=True)
        self.screenshare_button.pack(side='bottom', fill='both', expand=True)
        self.conection_label.pack(side='top', fill='both', expand=True)

    # def show_files(self, current_group):
    #     host_folder = os.path.join(current_group, str(self.host.number))
    #     self.files_label['text'] = 'Files at %s' % host_folder
    #     path_to_host_folder = os.path.join(basepath, host_folder)
    #     files_only_on_this_host = self.host.list_files(path_to_host_folder)
    #     path_to_all_folder = os.path.join(basepath, current_group, 'all')
    #     files_on_all_hosts = self.host.list_files(path_to_all_folder)
    #     if files_only_on_this_host:
    #         self.files.delete(0, 'end')  # delete previous entries
    #         self.files.insert('end', 'Files only on this host:')
    #         for name in files_only_on_this_host:
    #             if not name.startswith('.') and name != 'Readme.md':
    #                 self.files.insert('end', name)
    #     if files_on_all_hosts:
    #         self.files.insert('end', 'Files on all hosts:')
    #         for name in files_on_all_hosts:
    #             if not name.startswith('.') and name != 'Readme.md':
    #                 self.files.insert('end', name)

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
        self.projector_control_panel = tk.Frame(self.main_window)
        self.main_control_panel.pack(side='top', fill='x', expand=False)
        self.hosts_control_panel.pack(side='top', fill='both', expand=False)
        self.projector_control_panel.pack(side='top', fill='both', expand=False)

        self.group_label = tk.Label(self.main_control_panel, text='Select group: ')
        self.selected_group = tk.StringVar(self.main_control_panel)
        self.selected_group.trace('w', self.change_group)
        self.group = tk.OptionMenu(self.main_control_panel, self.selected_group, *groups)
        self.update_button = tk.Button(self.main_control_panel, text='Update Files on Hosts', command=self.update)
        self.check_connection_button = tk.Button(self.main_control_panel, text='Check connections', command=self.check_connections)
        self.run_or_quit_app_button = tk.Button(self.main_control_panel, text='Run Apps', command=self.run_or_quit_apps)
        self.start_syphon_button = tk.Button(self.main_control_panel, text='Start Syphon', command=self.start_syphon)
        self.start_checker_button = tk.Button(self.main_control_panel, text='Start Checker Apps', command=self.start_or_quit_checker_apps)
        #self.start_app_button = tk.Button(self.main_control_panel, text='Start App', command=self.start_app)

        self.group_label.pack(side='left', expand=True)
        self.group.pack(side="left", fill="x", expand=True)
        self.update_button.pack(side='left', expand=True)
        self.check_connection_button.pack(side='left', expand=True)
        self.run_or_quit_app_button.pack(side='left', expand=True)
        self.start_checker_button.pack(side='left', expand=True)
        self.start_syphon_button.pack(side='left', expand=True)
        #self.start_app_button.pack(side='left', expand=True)

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
                p = Projector(projector['name'], ip_address, projector['position'], projector['port'])
                projector_frame = ProjectorFrame(host_frame, p)
                projector_frame.pack(side='right', fill='both', expand=True)
                self.projector_frames.append(projector_frame)

        self.running = False
        self.checker_running = False
        self.selected_group.set('TeamTest')
        self.check_connections()

    def change_group(self, *args):
        group = self.selected_group.get()
        self.logger.info('Changed group to %s' % group)
        self.update_host_frames()  # TODO: maybe deprecated
        self.update_projector_frames()
        if not groups[group]['use_checker']:
            self.start_checker_button['state'] = 'disabled'
            self.start_syphon_button['state'] = 'disabled'
        else:
            self.start_checker_button['state'] = 'normal'
            self.start_syphon_button['state'] = 'normal'

    def update_host_frames(self):
        # TODO may be deprecated
        for host_frame in self.host_frames:
            # host_frame.show_files(self.selected_group.get())
            pass

    def update_projector_frames(self):
        for projector_frame in self.projector_frames:
            projector_frame.update_labels(self.selected_group.get())

    def check_connections(self):
        for host in self.host_frames:
            host.set_connection()

    def run_or_quit_apps(self):
        if self.running:
            self.quit_apps()
            self.running = False
            self.run_or_quit_app_button['text'] = 'Run Apps'
        else:
            self.start_apps()
            self.running = True
            self.run_or_quit_app_button['text'] = 'Quit Apps'

    # def run_or_quit(self):
    #     group_folder = os.path.join(basepath, self.selected_group.get())
    #     self.logger.info('Change directory to %s' % group_folder)
    #     os.chdir(group_folder)
    #     if self.running:
    #         action = 'quit'
    #         self.running = False
    #         self.run_or_quit_app_button['text'] = 'Run'
    #         self.logger.info('Executing ./project %s' % action)
    #         run_shell_command('./project %s' % action)
    #     else:
    #         action = 'run'
    #         self.running = True
    #         self.run_or_quit_app_button['text'] = 'Quit'
    #         self.logger.info('Executing ./project %s' % action)
    #         run_shell_command('./project %s' % action)

    def start_syphon(self):
        pass
    
    def start_apps(self):
        for projector_frame in self.projector_frames:
            projector_frame.start_app()

    def quit_apps(self):
        for projector_frame in self.projector_frames:
            projector_frame.quit_app()

    def start_checker_apps(self):
        for projector_frame in self.projector_frames:
            projector_frame.start_checker_app()
            # time.sleep(1)

    def quit_checker_apps(self):
        for projector_frame in self.projector_frames:
            projector_frame.quit_checker_app()

    def update(self):
        host_ips = ' '.join([hosts[host]['ip_address'] for host in hosts])
        source = basepath
        destination = basepath[:-1]  # no / in the end!
        cmd = 'prsync -r -v -H "%s" %s %s' % (host_ips, source, destination)
        self.logger.info(cmd)
        run_shell_command(cmd)

    def start_or_quit_checker_apps(self):
        if self.checker_running:
            self.quit_checker_apps()
            self.checker_running = False
            self.start_checker_button['text'] = 'Start Checker Apps'
        else:
            self.start_checker_apps()
            self.checker_running = True
            self.start_checker_button['text'] = 'Quit Checker Apps'


if __name__ == "__main__":
    root = tk.Tk()
    MutationGui(root)
    root.mainloop()
