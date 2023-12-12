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


def dir_func(client_socket):
    try:
        folder_name_bytes = Protocol.receive_(client_socket)
        logging.debug('received: ' + folder_name_bytes)
        print('folder_name_bytes: ' + folder_name_bytes)
        if not os.path.exists(folder_name_bytes):
            logging.warning('folder do not exist: ' + folder_name_bytes)
            Protocol.send_(client_socket, 'folder do not exist: ' + folder_name_bytes)
        else:
            files_list = glob.glob(rf'{folder_name_bytes}*.*')
            output = f"{files_list}"
            logging.debug(f'the files: {output} are in: {folder_name_bytes}')
            Protocol.send_(client_socket, output)
    except socket.error as err:
        Protocol.send_('received socket error while trying to dir: ' + folder_name_bytes)
        logging.error('received socket error while trying to dir' + str(err))


def delete_func(client_socket):
    try:
        file_name = Protocol.receive_(client_socket)
        print('file_name: ' + file_name)
        logging.debug('file name del: ' + file_name)
        os.remove(file_name)
        print(f"{file_name} has been removed successfully")
        logging.debug("File deleted successfully")
        Protocol.send_(client_socket, "File deleted successfully")

    except OSError as err:
        Protocol.send_(client_socket, 'received os error while trying to delete: ' + file_name)
        logging.error('received os error while trying to delete' + str(err))

    except socket.error as err:
        Protocol.send_(client_socket, 'received socket error while trying to delete: ' + file_name)
        logging.error('received socket error while trying to delete' + str(err))


def copy_func(client_socket):
    try:
        source = Protocol.receive_(client_socket)
        print('source: ' + source)
        destination = Protocol.receive_(client_socket)
        print('destination: ' + destination)
        shutil.copy(source, destination)
        Protocol.send_(client_socket, f"File {source} copied to {destination} successfully")

    except OSError as err:
        Protocol.send_(client_socket, f'received os error while trying to copy {source} to {destination}:')
        logging.error(f'received os error while trying to copy {source} to {destination}:' + str(err))
    except socket.error as err:
        Protocol.send_(client_socket, f'received socket error while trying to copy {source} to {destination}:')
        logging.error(f'received socket error while trying to copy {source} to {destination}:' + str(err))


def execute_func(client_socket):
    try:
        program_path = Protocol.receive_(client_socket)
        subprocess.call(program_path)
        Protocol.send_(client_socket, 'executed successfully')
    except OSError as err:
        logging.error(f'received os error while trying to execute {program_path}' + str(err))
        Protocol.send_(client_socket, f'received os error while trying to execute {program_path}')
    except socket.error as err:
        logging.error(f'received socket error while trying to execute {program_path}' + str(err))
        Protocol.send_(client_socket, f'received socket error while trying to execute {program_path}')


def take_screenshot_func(client_socket):
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
        logging.error('received socket error while trying to save screenshot: ' + str(err))
        Protocol.send_(client_socket, 'received socket error while trying to save screenshot')


def return_answer(request, client_socket):
    """
    :param: request
    :type: request str
    :return: dt_string | SERVER_NAME | random_number
    :rtype: str | int
    """

    if request == 'DIR':
        dir_func(client_socket)
    elif request == 'DELETE':
        delete_func(client_socket)
    elif request == 'COPY':
        copy_func(client_socket)
    elif request == 'EXECUTE':
        execute_func(client_socket)
    elif request == 'TAKE_SCREENSHOT':
        take_screenshot_func(client_socket)
    elif request == 'EXIT' or 'Error':
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
