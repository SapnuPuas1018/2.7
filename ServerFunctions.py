import socket
import logging
import glob
import os
import shutil
import Protocol
import subprocess
import pyautogui
import base64

FOLDER_PATH_FOR_SCREENSHOTS = r'C:\Users\nati2\OneDrive\Desktop\2.7\screen.jpg'


def dir_func(client_socket):
    """
    Retrieves a list of files in the specified directory and sends it to the client.

    :param client_socket: The client socket connected to the server.
    :type client_socket: socket.socket

    :return: A string containing the list of files in the directory.
    :rtype: str
    """
    try:
        folder_name_bytes = Protocol.receive_(client_socket)
        logging.debug('received: ' + folder_name_bytes)
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
    """
    Deletes the specified file.

    :param client_socket: The client socket connected to the server.
    :type client_socket: socket.socket

    :return: A message indicating the success or failure of the deletion.
    :rtype: str
    """
    try:
        file_name = Protocol.receive_(client_socket)
        logging.debug('file name del: ' + file_name)
        os.remove(file_name)
        logging.debug("File deleted successfully")
        Protocol.send_(client_socket, "File deleted successfully")

    except OSError as err:
        Protocol.send_(client_socket, 'received os error while trying to delete: ' + file_name)
        logging.error('received os error while trying to delete' + str(err))

    except socket.error as err:
        Protocol.send_(client_socket, 'received socket error while trying to delete: ' + file_name)
        logging.error('received socket error while trying to delete' + str(err))


def copy_func(client_socket):
    """
    Copies a file from the source to the destination.

    :param client_socket: The client socket connected to the server.
    :type client_socket: socket.socket

    :return: A message indicating the success or failure of the copy operation.
    :rtype: str
    """
    try:
        source = Protocol.receive_(client_socket)
        destination = Protocol.receive_(client_socket)
        shutil.copy(source, destination)
        Protocol.send_(client_socket, f"File {source} copied to {destination} successfully")

    except OSError as err:
        Protocol.send_(client_socket, f'received os error while trying to copy {source} to {destination}:')
        logging.error(f'received os error while trying to copy {source} to {destination}:' + str(err))
    except socket.error as err:
        Protocol.send_(client_socket, f'received socket error while trying to copy {source} to {destination}:')
        logging.error(f'received socket error while trying to copy {source} to {destination}:' + str(err))


def execute_func(client_socket):
    """
    Executes the specified program.

    :param client_socket: The client socket connected to the server.
    :type client_socket: socket.socket

    :return: A message indicating the success or failure of the execution.
    :rtype: str
    """
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
    """
    Takes a screenshot and sends it to the client.

    :param client_socket: The client socket connected to the server.
    :type client_socket: socket.socket

    :return: A base64-encoded string representing the screenshot.
    :rtype: str
    """
    try:
        image = pyautogui.screenshot()
        image.save(FOLDER_PATH_FOR_SCREENSHOTS)
        with open(FOLDER_PATH_FOR_SCREENSHOTS, 'rb') as image_file:
            base64_bytes = base64.b64encode(image_file.read())

            base64_string = base64_bytes.decode()
            Protocol.send_(client_socket, base64_string)
    except socket.error as err:
        logging.error('received socket error while trying to save screenshot: ' + str(err))
        Protocol.send_(client_socket, 'received socket error while trying to save screenshot')


def return_answer(request, client_socket):
    """
    Processes the client's request and returns the corresponding result.

    :param request: The client's request.
    :type request: str

    :param client_socket: The client socket connected to the server.
    :type client_socket: socket.socket

    :return: A message indicating the success or failure of the requested operation.
    :rtype: str
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