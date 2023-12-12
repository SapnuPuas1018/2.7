"""
author - Yuval Hayun
date   - 23/11/23
socket client
"""
import os
import socket
import logging
import Protocol
import base64
from io import BytesIO
from PIL import Image

logging.basicConfig(filename='my_log.log', level=logging.DEBUG)

SERVER_IP = '127.0.0.1'
SERVER_PORT = 16241
HEADER_LEN = 2
MAX_PACKET = 1024
COMMAND_SINGLE_PARAMETER_LIST = ['DIR', 'DELETE', 'EXECUTE']


def main():
    """
    main function
    :return: None
    """
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        my_socket.connect(('127.0.0.1', SERVER_PORT))
        logging.debug('connected')
        request = ''
        while request != 'EXIT':
            request = input('enter your request here: ')
            print(request)
            Protocol.send_(my_socket, request)
            if request in COMMAND_SINGLE_PARAMETER_LIST:
                folder_name = input(f'enter the file path ({request}): ')
                Protocol.send_(my_socket, folder_name)
                response = Protocol.receive_(my_socket)
                print(response)
            elif request == 'COPY':
                source = input('enter the file path that you want to copy: ')
                Protocol.send_(my_socket, source)
                destination = input('enter the destination: ')
                Protocol.send_(my_socket, destination)
            elif request == 'TAKE_SCREENSHOT':
                Protocol.send_(my_socket, request)
                response = Protocol.receive_(my_socket)
                decoded_string = base64.b64decode(response)
                try:
                    image = Image.open(BytesIO(decoded_string))
                    image.show()
                    image.close()
                except Exception as err:
                    logging.error('error in TAKE_SCREENSHOT' + str(err))
            elif request == 'EXIT':
                Protocol.send_(my_socket, request)
                response = Protocol.receive_(my_socket)
                print(response)
            else:
                print('invalid command')
                logging.debug('client entered an invalid request')
    except socket.error as err:
        logging.debug('received socket error ' + str(err))
    finally:
        my_socket.close()


if __name__ == '__main__':
    main()
