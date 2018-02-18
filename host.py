""" Module for functionality belonging to mutation hosts.

Copyright 2018
Author Elke Schaechtele <elke.schaechtele@stud.hfm-karlsruhe.de>
"""
import logging
from utils import run_shell_command, run_ssh_command


class Host(object):

    def __init__(self, number, ip_address):
        """ Initialisation of a host.

        :param (int) number: Any number used to identify the host in MUT.
        :param (str) ip_address: Ip address of the host.
        """
        self.ip_address = ip_address
        self.number = number
        self.logger = logging.getLogger(__name__)

    def open_screensharing(self):
        command = 'open vnc://%s' % self.ip_address
        self.logger.info('Try to open screen sharing for %s' % self.ip_address)
        run_shell_command(command)

    def list_files(self, path):
        """ List files found at given path on host.

        This method was used while the idea was to have not all files on every
        host. Since one and the same file folder is synchronized with every
        host, it is no longer used. It was still not deleted, as it might be
        desirable in the future to be able to list files on a specific path
        for a given host, e.g. for debugging purposes.
        """
        command = 'ls %s' % path
        self.logger.info('Listing files at %s' % path)
        out, error = run_ssh_command(command, self.ip_address)
        if 'Network is unreachable' in error:
            return ['No connection - no files!']
        else:
            files = [f for f in out.split('\t') if f != '']
            self.logger.info('Found the following files: %s' % files)
            return files

    def shutdown(self):
        command = 'sudo shutdown -h now'
        self.logger.info('Goint to shutdown %s' % self.ip_address)
        run_ssh_command(command, self.ip_address, sudo=True)

    def restart(self):
        command = 'sudo shutdown -r now'
        self.logger.info('Goint to restart %s' % self.ip_address)
        run_ssh_command(command, self.ip_address, sudo=True)
    
    def quit_any_apps(self, number=4):
        for x in range(number):
            cmd = """osascript -e 'tell application \\"System Events\\" to keystroke \\"q\\" using command down'"""
            run_ssh_command(cmd, self.ip_address)

    def reachable(self):
        """ Check whether the host is reachable via ssh.

        >>> host = Host(10, '127.0.0.1')
        >>> host.reachable() is False
        True

        :return: (bool) True, if host is reachable via ssh.
        """
        command = 'echo test'
        out, error = run_ssh_command(command, self.ip_address)
        if out:
            return True
        else:
            return False
