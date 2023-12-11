import logging
import socket

logging.basicConfig(filename='my_log_protocol.log', level=logging.DEBUG)

MAX_PACKET = 1024


def receive(my_socket):
    print('receiving...')
    response = ""
    length = ""
    msg = ""
    try:
        # Read the length of the message
        while True:
            response = my_socket.recv(1).decode()
            print('response1: ' + response)
            if response == "!":
                break
            length += response
            print('length: ' + length)

        if length != '':
            length = int(length)
            print('length: ' + str(length))

            # Receive the message
            while len(msg) < length:
                response = my_socket.recv(min(MAX_PACKET, length - len(msg))).decode()
                print('response2: ' + response)
                if response == "":
                    msg = ""
                    break
                msg += response
                print('msg: ' + msg)

    except:
        logging.error('received socket error: ')
    finally:
        return msg


def send(my_socket, msg):
    """
    :param my_socket:
    :return:
    """
    print('sending...')
    sent = 0
    try:
        # Construct the message with length and delimiter
        msg = str(len(msg)) + '!' + msg

        # Send the message
        while sent < len(msg):
            sent += my_socket.send(msg[sent:].encode())
        return True
    except socket.error as err:
        logging.error("received socket error: " + str(err))
        return False
