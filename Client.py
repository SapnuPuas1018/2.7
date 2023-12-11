"""
author - Yuval Hayun
date   - 23/11/23
socket client
"""
import os
import socket
import logging
import Protocol

logging.basicConfig(filename='my_log.log', level=logging.DEBUG)

SERVER_IP = '127.0.0.1'
SERVER_PORT = 16241
HEADER_LEN = 2
MAX_PACKET = 1024
COMMAND_SINGLE_PARAMETER_LIST = ['DIR', 'DELETE', 'EXECUTE']


def main():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        my_socket.connect(('127.0.0.1', SERVER_PORT))
        logging.debug('connected')
        request = ['', ]
        while request != 'EXIT':
            request = input('enter your request here: ')
            print(request)
            Protocol.send(my_socket, request)
            if request in COMMAND_SINGLE_PARAMETER_LIST:
                folder_name = input(f'enter the file path ({request}): ')
                Protocol.send(my_socket, folder_name)
                response = Protocol.receive(my_socket)
                print(response)

            # if request == 'DIR':
            #     folder_name = input('enter the folder path (DIR): ')
            #     Protocol.send(my_socket, folder_name)
            #     response = Protocol.receive(my_socket)
            #     print(response)
            # elif request == 'DELETE':
            #     file_name = input('enter the file path that you want to delete:')
            #     Protocol.send(my_socket, file_name)
            #     response = Protocol.receive(my_socket)
            #     print(response.decode())

            elif request == 'COPY':
                source = input('enter the file path that you want to copy: ')
                Protocol.send(my_socket, source)
                destination = input('enter the destination: ')
                Protocol.send(my_socket, destination)
            # elif request == 'EXECUTE':
            #     file_name = input('enter the file path that you want to execute:')
            #     Protocol.send(my_socket, file_name)
            #     response = Protocol.receive(my_socket)
            #     print(response)
            elif request == 'EXIT':
                my_socket.send(request.encode())
            else:
                print('invalid')
                logging.debug('client entered an invalid request')
    except socket.error as err:
        logging.debug('received socket error ' + str(err))
    finally:
        my_socket.close()


if __name__ == '__main__':
    main()
