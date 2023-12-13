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


FOLDER_PATH_FOR_SCREENSHOTS = r'C:\Users\nati2\OneDrive\Desktop\2.7\screen.jpg'


def dir_func(client_socket):
    """
    Retrieves a list of files in a specified folder and sends it to the client.

    :param client_socket: The client socket for communication.
    :type client_socket: socket.socket

    :return: If the specified folder exists, a list of files in the folder is sent to the client.
             If the folder does not exist, a warning message is sent to the client.
    :rtype: None
    """
    try:
        # Receive the folder name from the client
        folder_name_bytes = Protocol.receive_(client_socket)
        logging.debug('folder_name_bytes' + folder_name_bytes)

        # Check if the folder exists
        if not os.path.exists(folder_name_bytes):
            logging.warning('folder do not exist: ' + folder_name_bytes)
            Protocol.send_(client_socket, f'folder {folder_name_bytes} do not exist')
        else:
            # Get the list of files in the folder
            files_list = glob.glob(rf'{folder_name_bytes}\*.*')
            output = f"{files_list}"
            logging.debug(f'the files: {output} are in: {folder_name_bytes}')

            # Send the list of files to the client
            Protocol.send_(client_socket, output)
    except socket.error as err:
        logging.error('received socket error in dir ' + str(err))


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
        Protocol.send_(client_socket, 'error while trying to delete: ' + file_name)
        logging.error('received os error while trying to delete' + str(err))

    except socket.error as err:
        Protocol.send_(client_socket, 'error while trying to delete: ' + file_name)
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
        Protocol.send_(client_socket, f'error while trying to copy {source} to {destination}:')
        logging.error(f'received os error while trying to copy {source} to {destination}:' + str(err))
    except socket.error as err:
        Protocol.send_(client_socket, f'error while trying to copy {source} to {destination}:')
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
        Protocol.send_(client_socket, f'error while trying to execute {program_path}')
    except socket.error as err:
        logging.error(f'received socket error while trying to execute {program_path}' + str(err))
        Protocol.send_(client_socket, f'error while trying to execute {program_path}')


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
        Protocol.send_(client_socket, 'error while trying to save screenshot')


def exit_func(client_socket):
    try:
        Protocol.send_(client_socket, 'Goodbye')
    except socket.error as err:
        logging.error('received socket error while trying to exit: ' + str(err))
        Protocol.send_(client_socket, 'error while trying exit')


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
        exit_func(client_socket)
        return 'exit'
