"""
Protocol Functions

:author: Yuval Hayun
:date: 12/12/23
"""

import logging
import socket

logging.basicConfig(filename='my_log_protocol.log', level=logging.DEBUG)

MAX_PACKET = 1024
LENGTH_FIELD_SIZE = 10


def receive_(my_socket):
    """
    Receives and decodes a message from the given socket.

    :param: my_socket: The socket to receive the message from.
    :type: my_socket: socket.socket

    :return: The decoded message.
    :rtype: str
    """
    try:
        length_bytes = my_socket.recv(LENGTH_FIELD_SIZE)
        if not length_bytes:
            return 'Error'
        length = int(length_bytes.decode())
        data_bytes = my_socket.recv(length)
        data = data_bytes.decode()
        return data
    except socket.error as err:
        logging.error('received socket error' + str(err))


def send_(my_socket, data):
    """
    Encodes and sends a message through the given socket.

    :param my_socket: The socket to send the message through.
    :type my_socket: socket. Socket

    :param data: The message to be sent.
    :type data: str

    :return: None
    """
    data_bytes = data.encode()
    length = len(data_bytes)
    length = str(length).zfill(LENGTH_FIELD_SIZE)
    full_msg = length.encode() + data_bytes
    try:
        my_socket.send(full_msg)
    except socket.error as err:
        logging.error('received socket error: ' + str(err))
