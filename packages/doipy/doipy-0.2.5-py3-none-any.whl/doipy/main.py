import json
from typing import Annotated
import typer
from jsonschema import ValidationError

from doipy import hello, list_operations, create, create_fdo, search, get_design, get_init_data
from doipy.constants import DOType, ResponseStatus
from doipy.exceptions import AuthenticationException, InvalidRequestException
from doipy.models import FdoInput, DoInput
from doipy.server import server

app = typer.Typer()


@app.command(name='hello')
def hello_command(service: Annotated[str, typer.Argument(help='the PID identifying a data service in the service '
                                                              'registry')]):
    """
    Implements 0.DOIP/Op.Hello: An operation to allow a client to get information about the DOIP service.
    """

    # call hello and receive response
    response = hello(service)
    # print response
    print(json.dumps(response, indent=2))


@app.command(name='list_operations')
def list_operations_command(service: Annotated[str, typer.Argument(help='the PID identifying a data service in the '
                                                                        'service registry')]):
    """
    Implements 0.DOIP/Op.ListOperations: An operation to request the list of operations that can be invoked on the
    target DO.
    """
    # call list_operations and receive response
    response = list_operations(service)
    # print response
    print(json.dumps(response, indent=2))


@app.command(name='create')
def create_command(
        service: Annotated[str, typer.Argument(help='the PID identifying a data service in the service registry')],
        input_file: Annotated[typer.FileText, typer.Argument(help='A file containing a JSON which follows a specific '
                                                                  'JSON schema. The file contains a bit-sequence and'
                                                                  'corresponding metadata which together form a DO.')],
        client_id: Annotated[str, typer.Option(help='The identifier of the user in Cordra')] = None,
        username: Annotated[str, typer.Option(help='Username of the user in Cordra')] = None,
        token: Annotated[str, typer.Option(help='Token generated in Cordra')] = None):

    """Implements 0.DOIP/Op.Create: An operation to create a digital object (containing at most one data bit-sequence)
    within the DOIP service. The target of a creation operation is the DOIP service itself."""

    # read the input
    input_json = json.load(input_file)

    # validate the input against the JSON input schema and define data structure for DO input
    try:
        do_input = DoInput.parse(input_json)
    except ValidationError as error:
        print(str(error))
        raise typer.Exit()

    # create the DO
    # if token, username and client_id are provided, authentication is successful if and only if token is correct
    # if username and client_id are both provided, authentication is successful if and only if client_id is correct
    try:
        if not token and (client_id or username):
            password = typer.prompt('Password', hide_input=True)
            response = create(service, DOType.DO.value, do_input.file, do_input.md, password, client_id, username,
                              token)
        else:
            response = create(service, do_type=DOType.DO.value, bitsq=do_input.file, metadata=do_input.md,
                              client_id=client_id, username=username, token=token)

    # in case that the DOIP response status is not success, raise an exception and terminate the program
    except AuthenticationException as error:
        print(str(error))
        raise typer.Exit()
    except InvalidRequestException as error:
        details = error.args[0][0]
        print(f'{details['status']} {ResponseStatus(details['status']).name}')
        print(details['output']['message'])
        raise typer.Exit()

    print(json.dumps(response, indent=2))


@app.command(name='create_fdo')
def create_fdo_command(
        service: Annotated[str, typer.Argument(help='the PID identifying a data service in the service registry')],
        input_file: Annotated[typer.FileText, typer.Argument(help='A file containing a JSON which follows a specific '
                                                                  'JSON schema. The file contains data bit-sequences, '
                                                                  'metadata bit-sequences and the metadata that should '
                                                                  'be written into the corresponding PID records.')],
        client_id: Annotated[str, typer.Option(help='The identifier of the user in Cordra')] = None,
        username: Annotated[str, typer.Option(help='Username of the user')] = None,
        token: Annotated[str, typer.Option(help='Token generated in Cordra')] = None):
    """Create a new FAIR Digital Object (FDO) from data and metadata files."""

    # read the input
    input_json = json.load(input_file)

    # validate the input against the JSON input schema and create an instance of FdoInput class
    try:
        fdo_input = FdoInput.parse(input_json)
    except ValidationError as error:
        # if validation against JSON schema fails, raise an exception
        print(str(error))
        raise typer.Exit()

    # Create the FDO
    try:
        if not token and (client_id or username):
            password = typer.prompt('Password', hide_input=True)
            response = create_fdo(service, fdo_input, password, client_id, username, token)
        else:
            response = create_fdo(service, fdo_input=fdo_input, client_id=client_id, username=username, token=token)

    except AuthenticationException as error:
        print(str(error))
        raise typer.Exit()
    # in case that the DOIP response is not success, raise an exception and terminate the program
    except InvalidRequestException as error:
        details = error.args[0][0]
        print(f'{details['status']} {ResponseStatus(details['status']).name}')
        print(details['output']['message'])
        raise typer.Exit()

    print(json.dumps(response, indent=2))


@app.command(name='search')
def search_command(query: Annotated[str, typer.Argument(help='query')],
                   username: Annotated[str, typer.Option(help='username')] = None,
                   password: Annotated[str, typer.Option(help='password')] = None):
    """Implements 0.DOIP/Op.Search"""
    response = search(query, username, password)
    print(json.dumps(response, indent=2))


@app.command(name='get_design')
def get_design_command():
    """Implements 20.DOIP/Op.GetDesign (see https://www.cordra.org)"""
    response = get_design()
    print(json.dumps(response, indent=2))


@app.command(name='get_init_data')
def get_init_data_command():
    """Implements 20.DOIP/Op.GetInitData (see https://www.cordra.org)"""
    response = get_init_data()
    print(json.dumps(response, indent=2))


@app.command(name='doip_server')
def doip_server_command(hostname: Annotated[str, typer.Argument(help='hostname')],
                        port: Annotated[int, typer.Argument(help='port')],
                        privkey: Annotated[str, typer.Argument(help='privkey')],
                        cert: Annotated[str, typer.Argument(help='cert')]):
    """Starts a DOIP server"""
    server(hostname, port, privkey, cert)
