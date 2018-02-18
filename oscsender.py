""" Module containing function for sending of osc messages.

Copyright 2018
Author Elke Schaechtele <elke.schaechtele@stud.hfm-karlsruhe.de>
"""
import OSC  # pip install pyOSC
import logging

logger = logging.getLogger(__name__)


def send_osc(ip_address, port, address, arguments):
    """ Send an osg message to the host with given ip_address on given port.

    >>> send_osc('127.0.0.1', 22, '/test', [1, 2])

    :param (str) ip_address: Ip address of osc host.
    :param (int) port: Port of osc host.
    :param (str) address: Beginning of osc message, starting with '/'
    :param (list) arguments: The arguments for the osc message.
    :return:
    """
    msg = OSC.OSCMessage()
    msg.setAddress(address)
    for argument in arguments:
        msg.append(argument)

    osc_client = OSC.OSCClient()
    osc_client.connect((ip_address, port))
    logger.info('Sending %s to %s on %s' % (msg, ip_address, port))
    osc_client.send(msg)
    # TODO: return something?
