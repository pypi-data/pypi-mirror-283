import uuid
from pathlib import Path

from doipy.exceptions import InvalidRequestException, AuthenticationException
from doipy.constants import DOIPOperation, ResponseStatus
from doipy.socket_utils import create_socket, send_message, finalize_socket, finalize_segment, read_response, \
    get_settings


def hello(service: str):
    # get service settings
    target_id, ip, port = get_settings(service)
    # create request message
    message = {
        'targetId': f'{target_id}',
        'operationId': DOIPOperation.HELLO.value
    }
    # send request and return response
    with create_socket(ip, port) as ssl_sock:
        send_message(message, ssl_sock)
        finalize_segment(ssl_sock)
        finalize_socket(ssl_sock)
        response = read_response(ssl_sock)
        return response


def list_operations(service):
    # get service settings
    target_id, ip, port = get_settings(service)
    # create request message
    message = {
        'targetId': f'{target_id}',
        'operationId': DOIPOperation.LIST_OPERATION.value
    }

    # send request and read response
    with create_socket(ip, port) as ssl_sock:
        send_message(message, ssl_sock)
        finalize_segment(ssl_sock)
        finalize_socket(ssl_sock)
        response = read_response(ssl_sock)
        return response


def create(service: str, do_type: str, bitsq: Path, metadata: dict, password: str = None, client_id: str = None,
           username: str = None, token: str = None):

    # get service settings
    target_id, ip, port = get_settings(service)

    # check that either a username, password or token is provided
    if not username and not client_id and not token:
        raise AuthenticationException('Provide token, username or client_id')

    with create_socket(ip, port) as ssl_sock:

        # target id and operation id
        message_1 = {
            'targetId': f'{target_id}',
            'operationId': DOIPOperation.CREATE.value
        }

        # authentication
        if token:
            message_1['authentication'] = {
                'token': token
            }
        elif client_id:
            message_1['clientId'] = client_id
            message_1['authentication'] = {
                'password': password
            }
        else:
            message_1['authentication'] = {
                'username': username,
                'password': password
            }

        send_message(message_1, ssl_sock)
        finalize_segment(ssl_sock)

        # create a DO of type document in Cordra for the file which is added
        message_2 = {
            'type': do_type,
            'attributes': {
                'content': {
                    'id': '',
                    'name': 'digital object'
                }
            }
        }
        # add metadata to DO
        if metadata:
            message_2['attributes']['content'] = message_2['attributes']['content'] | metadata

        # add information on files to DO
        if bitsq:
            filename = bitsq.name
            my_uuid = str(uuid.uuid4())
            message_2['elements'] = [
                {
                    'id': my_uuid,
                    'type': 'text/plain',
                    'attributes': {
                        'filename': filename
                    }
                }
            ]

        send_message(message_2, ssl_sock)
        finalize_segment(ssl_sock)

        if bitsq:
            # send id
            message_3 = {
                'id': my_uuid
            }
            send_message(message_3, ssl_sock)
            finalize_segment(ssl_sock)

            # send content of files
            buffer_size = 1024
            with open(bitsq, 'rb') as f:
                while bytes_read := f.read(buffer_size):
                    ssl_sock.sendall(bytes_read)
                finalize_segment(ssl_sock)

        finalize_socket(ssl_sock)

        response = read_response(ssl_sock)
        if response[0]['status'] == ResponseStatus.SUCCESS.value:
            return response
        raise InvalidRequestException(response)


def update(service: str, client_id: str, password: str, do_type: str):
    # TODO fix message

    # get service settings
    target_id, ip, port = get_settings(service)

    with create_socket(ip, port) as ssl_sock:
        message = {
            'clientId': client_id,
            'targetId': target_id,
            'operationId': DOIPOperation.UPDATE.value,
            'authentication': {
                'password': password
            }
        }
        send_message(message, ssl_sock)
        string1 = f'https://cordra.testbed.pid.gwdg.de/objects/{target_id}?payload=file'
        string2 = f'https://cordra.testbed.pid.gwdg.de/objects/{target_id}'
        message = {
            'type': do_type,
            'attributes': {
                'content': {
                    'id': '',
                    'Payload': string1,
                    'Metadata': string2
                }
            }
        }
        send_message(message, ssl_sock)
        finalize_socket(ssl_sock)
        response = read_response(ssl_sock)
        return response


def search(service: str, query: str = 'type:Document', username: str = None, password: str = None):
    # TODO fix message

    # get service settings
    target_id, ip, port = get_settings(service)

    message = {
        'targetId': f'{target_id}',
        'operationId': DOIPOperation.SEARCH.value,
        'attributes': {
            'query': query
        }
    }
    if username and password:
        message['authentication'] = {
            'username': username,
            'password': password
        }

    with create_socket(ip, port) as ssl_sock:
        send_message(message, ssl_sock)
        finalize_socket(ssl_sock)
        response = read_response(ssl_sock)
        return response

# delete
# retrieve
