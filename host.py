import logging
from utils import run_shell_command, run_ssh_command


class Host(object):

    def __init__(self, number, ip_address, projectors=None):
        """

        :param number:
        :param ip_address: str
        :param projectors:
        """
        self.ip_address = ip_address
        self.number = number
        self.projectors = projectors
        self.logger = logging.getLogger(__name__)

    def open_screensharing(self):
        command = 'open vnc://%s' % self.ip_address
        self.logger.info('Try to open screen share for %s' % self.ip_address)
        run_shell_command(command)

    def open_monitor_settings(self):
        # run applescript
        pass

    def list_files(self, path):
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
        run_ssh_command(command, self.ip_address)

    def restart(self):
        command = 'sudo shutdown -r now'
        self.logger.info('Goint to restart %s' % self.ip_address)
        run_ssh_command(command, self.ip_address)

    def rechable(self):
        """

        >>> host = Host(10, '127.0.0.1')
        >>> host.rechable() is False
        True

        :return:
        """
        command = 'echo test'
        out, error = run_ssh_command(command, self.ip_address)
        if out:  # TODO: maxbe specify more direct
            return True
        else:
            return False
