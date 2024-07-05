from doipy.actions.doip import create
from doipy.constants import DOIPOperation, DOType, TypeInstance, TypeIdentifier, ResponseStatus
from doipy.exceptions import InvalidRequestException, AuthenticationException
from doipy.models import FdoInput
from doipy.socket_utils import create_socket, send_message, finalize_segment, finalize_socket, read_response, \
    get_settings


def create_fdo(service: str, fdo_input: FdoInput, password: str = None, client_id: str = None, username: str = None,
               token: str = None):

    # check that either a username, password or token is provided
    if not username and not client_id and not token:
        raise AuthenticationException('Provide token, username or client_id')

    # get service settings
    target_id, ip, port = get_settings(service)

    with create_socket(ip, port) as ssl_sock:
        message_1 = {
            'targetId': f'{target_id}',
            'operationId': DOIPOperation.CREATE.value,
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

        message_2 = {
            'type': DOType.FDO.value,
            'attributes': {
                'content': {
                    'id': '',
                    # FDO_Profile_Ref: mandatory
                    TypeIdentifier.FDO_PROFILE_REF.value: TypeInstance.FDO_PROFILE_REF_VAL.value,
                    # FDO_Type_Ref: mandatory
                    TypeIdentifier.FDO_TYPE_REF.value: TypeInstance.FDO_TYPE_REF_VAL.value
                }
            }
        }
        # create the data DOs
        if fdo_input.data_bit_sequences:
            data_refs = []
            for item in fdo_input.data_bit_sequences:
                response = create(service, DOType.DO.value, item.file, item.md, password, client_id, username, token)
                data_ref = response[0]['output']['id']
                data_refs.append(data_ref)
            message_2['attributes']['content'][TypeIdentifier.FDO_DATA_REFS.value] = data_refs

        # create the metadata DO
        if fdo_input.metadata_bit_sequence:
            response = create(service, DOType.DO.value, fdo_input.metadata_bit_sequence.file,
                              fdo_input.metadata_bit_sequence.md, password, client_id, username, token)
            metadata_ref = response[0]['output']['id']
            message_2['attributes']['content'][TypeIdentifier.FDO_MD_REFS.value] = metadata_ref

        # create the FDO
        send_message(message_1, ssl_sock)
        finalize_segment(ssl_sock)

        send_message(message_2, ssl_sock)
        finalize_segment(ssl_sock)
        finalize_socket(ssl_sock)

        response = read_response(ssl_sock)
        if response[0]['status'] == ResponseStatus.SUCCESS.value:
            return response
        raise InvalidRequestException(response)
