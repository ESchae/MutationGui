""" Module containing functions for the execution of bash commands.

Copyright 2018
Author Elke Schaechtele <elke.schaechtele@stud.hfm-karlsruhe.de>
"""
import subprocess
import shlex
import logging

logger = logging.getLogger(__name__)


def run_shell_command(command):
    """ Run any given command as shell command.

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


def run_ssh_command(command, ip_address, sudo=False):
    """ Execute the given command via ssh on a host with given ip address.

    # TODO: Try ssh with sudo
    >>> cmd = 'sudo shutdown -r now'
    >>> run_ssh_command(cmd, '192.168.0.13')

    :param command:
    :param ip_address:
    :return:
    """
    # -tt is needed because stdin is not a terminal
    # -o ConnectTimeout=1 lets ssh wait only one second for the connection
    # this is used to speed up the process, if a connection can not be
    # established
    if sudo:
        # -t is used to show the password promt in terminal
        # TODO: Works in terminal, but not if evoked via python script...
        command = 'ssh -tt -t -o ConnectTimeout=1 %s "%s"' % (ip_address,
                                                              command)
    else:
        command = 'ssh -tt -o ConnectTimeout=1 %s "%s"' % (ip_address,
                                                           command)
    return run_shell_command(command)


# TODO: Instead of ssh, pssh could be tried (python library exists)
