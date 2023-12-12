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
import pyautogui
import base64


logging.basicConfig(filename='my_log.log', level=logging.DEBUG)

IP = '127.0.0.1'
PORT = 16241
QUEUE_LEN = 1
MAX_PACKET = 1024
SHORT_SIZE = 2
FOLDER_PATH_FOR_SCREENSHOTS = r'C:\Users\nati2\OneDrive\Desktop\2.7\screen.jpg'


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
        except socket.error as err:
            logging.debug('folder not found' + str(err))
    elif request == 'DELETE':
        try:
            file_name = Protocol.receive_(client_socket)
            logging.debug('file name del: ' + file_name)
            os.remove(file_name)
            print(f"{file_name} has been removed successfully")
            logging.debug("File deleted successfully.")
            Protocol.send_(client_socket, b"File deleted successfully.")
        except socket.error as err:
            logging.debug('file not found' + str(err))
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
    elif request == 'TAKE_SCREENSHOT':
        try:
            image = pyautogui.screenshot()
            image.save(FOLDER_PATH_FOR_SCREENSHOTS)
            with open(FOLDER_PATH_FOR_SCREENSHOTS, 'rb') as image_file:
                base64_bytes = base64.b64encode(image_file.read())
                print(base64_bytes)

                base64_string = base64_bytes.decode()
                print(base64_string)
                Protocol.send_(client_socket, base64_string)
        except socket.error as err:
            logging.error(f'received socket error while trying to save screenshot {image}' + str(err))
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
                    request = Protocol.receive_(client_socket)
                    print('request: ' + request)
                    logging.debug('server received: ' + request)
                    response = return_answer(request, client_socket)
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
