"""
author - Yuval Hayun
date   - 23/11/23
socket server
"""
import socket
import logging
import glob
import os
import shutil
import Protocol
import subprocess

logging.basicConfig(filename='my_log.log', level=logging.DEBUG)

IP = '127.0.0.1'
PORT = 16241
QUEUE_LEN = 1
MAX_PACKET = 1024
SHORT_SIZE = 2


def return_answer(request, client_socket):
    """
    :param: request
    :type: request str
    :return: dt_string | SERVER_NAME | random_number
    :rtype: str | int
    """
    print('request: ' + request)
    if request == 'DIR':
        try:
            folder_name_bytes = Protocol.receive_(client_socket)
            print(folder_name_bytes)
            logging.debug('folder_name_bytes' + folder_name_bytes)
            x = glob.glob(rf'{folder_name_bytes}\*.*')
            print(x)
            output = f"{x}"
            logging.debug("output: " + output)
            Protocol.send_(client_socket, output)
            return x
        except socket.error as err:
            logging.debug('folder not found')
    elif request == 'DELETE':
        try:
            #file_name = client_socket.recv(MAX_PACKET).decode()
            file_name = Protocol.receive_(client_socket)
            logging.debug('file name del: ' + file_name)
            os.remove(file_name)
            print(f"{file_name} has been removed successfully")
            logging.debug("File deleted successfully.")
            #client_socket.send(b"File deleted successfully.")
            Protocol.send_(client_socket, b"File deleted successfully.")
        except socket.error as err:
            logging.debug('file not found')
    elif request == 'COPY':
        try:
            source = Protocol.receive_(client_socket)
            print('source: ' + source)
            destination = Protocol.receive_(client_socket)
            print('destination: ' + destination)
            shutil.copy(source, destination)
        except socket.error as err:
            logging.error(f'received socket error while trying to copy {source} to {destination}:' + err)
    elif request == 'EXECUTE':
        try:
            program_path = Protocol.receive_(client_socket)
            print('program_path: ' + program_path)
            subprocess.call(program_path)
            Protocol.send_(client_socket, 'executed')
        except socket.error as err:
            logging.error(f'received socket error while trying to execute {program_path}' + str(err))
    elif request == 'EXIT':
        return 'exit'


def main():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        my_socket.bind(('127.0.0.1', PORT))
        my_socket.listen(QUEUE_LEN)
        logging.debug('waiting for connection...')
        while True:
            client_socket, client_address = my_socket.accept()
            response = ''
            try:
                while response != 'exit':
                    #request = client_socket.recv(MAX_PACKET).decode()
                    request = Protocol.receive_(client_socket)
                    print('request: ' + request)
                    logging.debug('server received: ' + request)
                    response = return_answer(request, client_socket)
                    response = str(response)
                    print('response: ' + response)
            except socket.error as err:
                logging.debug('received socket error on client socket' + str(err))
            finally:
                client_socket.close()
                logging.debug('user disconnected')
    except socket.error as err:
        logging.debug('received socket error on server socket' + str(err))
    finally:
        my_socket.close()


if __name__ == '__main__':
    main()
