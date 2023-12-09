"""
author - Yuval Hayun
date   - 23/11/23
socket client
"""
import os
import socket
import logging

logging.basicConfig(filename='my_log.log', level=logging.DEBUG)

SERVER_IP = '127.0.0.1'
SERVER_PORT = 16241
HEADER_LEN = 2
MAX_PACKET = 1024


def protocol(my_socket):
    """
    :param my_socket:
    :return:
    """
    response = ''
    message_len = ''
    while response != '!':
        message_len += response
        response = my_socket.recv(1).decode()
    response = ''
    rounds_num = int(int(message_len) / MAX_PACKET)
    if int(int(message_len) % MAX_PACKET) != 0:
        rounds_num += 1
    for i in range(rounds_num):
        response += my_socket.recv(MAX_PACKET).decode()
    print(response)


def main():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        my_socket.connect(('127.0.0.1', SERVER_PORT))
        logging.debug('connected')
        request = ""
        while request != "EXIT":
            request = input('enter your request here: ')
            my_socket.send(request.encode())
            if request == 'DIR':
                file_name = input('enter the file name (DIR): ')
                my_socket.send(file_name.encode())
            elif request == 'DELETE':
                file_name = input('enter the file name that you want to delete: ')
                my_socket.send(file_name.encode())
            elif request == 'EXIT':
                my_socket.send(request.encode())
                protocol(my_socket)
            else:
                print('invalid')
                logging.debug('client entered an invalid request')
    except socket.error as err:
        logging.debug('received socket error ' + str(err))
    finally:
        my_socket.close()


if __name__ == '__main__':
    main()
