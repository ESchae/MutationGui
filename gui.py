import tkinter as tk
from config import hosts, groups, basepath
from host import Host
import logging, os
from datetime import datetime
from utils import run_shell_command, run_ssh_command

logging.basicConfig(level=logging.INFO)

class MainControlFrame(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.group_label = tk.Label(self, text='Select group: ')
        self.selected_group = tk.StringVar(self)
        self.selected_group.trace('w', self.change_group)
        self.selected_group.set('TeamTest')  # default
        self.group = tk.OptionMenu(self, self.selected_group, *groups)

        self.group_label.pack(side='left', expand=True)
        self.group.pack(side="right", fill="both", expand=True)

    def change_group(self, *args):
        print(self.selected_group.get())


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
        self.files = tk.Listbox(self)
        self.files_label = tk.Label(self, text='Files at ')

        # show connection info
        self.conection_label = tk.Label(self, text='__check connection__')

        self.label.pack(side='top', fill='x', expand=True)
        self.files_label.pack(side='top', fill='x', expand=True)
        self.files.pack(side='left')
        self.shutdown_button.pack(side='bottom', fill='both', expand=True)
        self.restart_button.pack(side='bottom', fill='both', expand=True)
        self.screenshare_button.pack(side='bottom', fill='both', expand=True)
        self.conection_label.pack(side='top', fill='both', expand=True)

    def show_files(self, current_group):
        host_folder = os.path.join(current_group, self.host.number)
        self.files_label['text'] = 'Files at %s' % host_folder
        path_to_host_folder = os.path.join(basepath, host_folder)
        files_only_on_this_host = self.host.list_files(path_to_host_folder)
        path_to_all_folder = os.path.join(basepath, current_group, 'all')
        files_on_all_hosts = self.host.list_files(path_to_all_folder)
        if files_only_on_this_host:
            self.files.delete(0, 'end')  # delete previous entries
            self.files.insert('end', 'Files only on this host:')
            for name in files_only_on_this_host:
                if not name.startswith('.') and name != 'Readme.md':
                    self.files.insert('end', name)
        if files_on_all_hosts:
            self.files.insert('end', 'Files on all hosts:')
            for name in files_on_all_hosts:
                if not name.startswith('.') and name != 'Readme.md':
                    self.files.insert('end', name)
            

    def set_connection(self):
        time = datetime.now().time().replace(microsecond=0)
        if self.host.rechable():
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
        self.hosts_control_panel.pack(side='bottom', fill='both', expand=False)

        self.group_label = tk.Label(self.main_control_panel, text='Select group: ')
        self.selected_group = tk.StringVar(self.main_control_panel)
        self.selected_group.trace('w', self.change_group)
        self.group = tk.OptionMenu(self.main_control_panel, self.selected_group, *groups)
        self.update_button = tk.Button(self.main_control_panel, text='Update', command=self.update)
        self.check_connection_button = tk.Button(self.main_control_panel, text='Check connections', command=self.check_connections)

        self.group_label.pack(side='left', expand=True)
        self.group.pack(side="left", fill="x", expand=True)
        self.update_button.pack(side='left', expand=True)
        self.check_connection_button.pack(side='left', expand=True)

        self.host_frames = []

        for host_number in hosts:
            ip_addess = hosts[host_number]
            host = Host(host_number, ip_addess)
            host_frame = HostFrame(self.hosts_control_panel, host)
            host_frame.pack(side='left', fill='both', expand=True)
            self.host_frames.append(host_frame)

    def change_group(self, *args):
        self.logger.info('Changed group to %s' % self.selected_group.get())
        self.update_host_frames()

    def update_host_frames(self):
        for host_frame in self.host_frames:
            host_frame.show_files(self.selected_group.get())

    def check_connections(self):
        for host in self.host_frames:
            host.set_connection()

    def update(self):
        # prsync -r -v -o $logOutDir -e $logErrorDir -H "${hosts[*]}" $sourcef $destination
        # see utils...
        # copy_to_all_hosts(files, ip_addresses)
        host_ips = ' '.join(hosts.values())
        source = basepath
        destination = basepath[:-1]  # no / in the end!
        #self.logger.info(run_ssh_command('echo $(pwd)/$line', '192.168.0.10'))
        #self.logger.info(run_ssh_command('ls', '192.168.0.10'))
        # TODO: show files in all
        cmd = 'prsync -r -v -H "%s" %s %s' % (host_ips, source, destination)
        self.logger.info(cmd)
        run_shell_command(cmd)
        


if __name__ == "__main__":
    root = tk.Tk()
    MutationGui(root)
    root.mainloop()
