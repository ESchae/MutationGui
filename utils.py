import subprocess
import shlex, errno
import logging
#from pssh.pssh_client import ParallelSSHClient  # pip install parallel-ssh
#from pssh.utils import enable_logger, logger
#from gevent import joinall

#pssh_logger = logger
#enable_logger(pssh_logger)
logger = logging.getLogger(__name__)  # general purpose logger


def run_shell_command(command):
    """

    Note: This will not work for commands that need to be executed with
    root privileges (using sudo). For Mutation this is only true for shutdown
    and restart, hence the following was done on all hosts:

    $ sudo chmod u+s /sbin/shutdown
    $ sudo chmod u+s /sbin/reboot

    This allows regular users to run the shutdown command as root.

    >>> out, err = run_shell_command('echo test')
    >>> print(out)
    test
    <BLANKLINE>
    >>> print(run_shell_command('x'))
    x is no valid command

    :param command:
    :return:
    """
    try:
        logger.debug('Try to execute %s' % command)
        process = subprocess.Popen(shlex.split(command),
                                   shell=False,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        out, error = process.communicate()
        out = out.decode('utf-8')
        error = error.decode('utf-8')
        if out:
            logger.info('Out: %s' % out.strip())
        if process.returncode != 0:
            logger.error(error.strip())
        return out, error
    except:  # occurs if no valid command was given
        logger.info('%s is no valid command' % command)
        return '%s is no valid command' % command


def run_ssh_command(command, ip_address):
    """

    # TODO: Try those
    >>> cmd = 'sudo shutdown -r now'
    >>> run_ssh_command(cmd, '192.168.0.13')

    :param command:
    :param ip_address:
    :return:
    """
    # -tt is needed because stdin is not a terminal
    # -o ConnectTimeout=2 lets ssh wait only two seconds for the connection
    command = 'ssh -tt -o ConnectTimeout=1 %s "%s"' % (ip_address, command)
    return run_shell_command(command)


"""
def copy_to_all_hosts(files, ip_addresses):
    client = ParallelSSHClient(ip_addresses)
    cmds = client.copy_file('../test', 'test_dir/test', recurse=True)  # todo: try with files - maybe problem with list?
    joinall(cmds, raise_error=True)
"""
