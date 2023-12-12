import logging
import socket

logging.basicConfig(filename='my_log_protocol.log', level=logging.DEBUG)

MAX_PACKET = 1024
LENGTH_FIELD_SIZE = 10


def receive_(my_socket):
    try:
        length_bytes = my_socket.recv(LENGTH_FIELD_SIZE)
        if not length_bytes:
            return "Error"
        length = int(length_bytes.decode())
        data_bytes = my_socket.recv(length)
        data = data_bytes.decode()
        return data
    except socket.error as err:
        logging.error('received socket error' + str(err))


def send_(my_socket, data):
    data_bytes = data.encode()
    length = len(data_bytes)
    length = str(length).zfill(LENGTH_FIELD_SIZE)
    full_msg = length.encode() + data_bytes
    try:
        my_socket.send(full_msg)
    except socket.error as err:
        logging.error('received socket error: ' + str(err))
