# DOIPY

Doipy is a Python wrapper for communication using the Digital Object Interface Protocol (DOIP) in its current
[specification v2.0](https://www.dona.net/sites/default/files/2018-11/DOIPv2Spec_1.pdf).

It supports the Basic Operations `hello`, `create`, `retrieve`, `update`, `delete`, `search`, and `list_operations`.
Extended Operations implemented by specific repository software are and will be included in the future.

## Install

Simply run

```shell
$ pip install doipy
```

## Usage

### Getting Started

This `doipy` package has several methods. Please use `doipy --help` to list all available methods.

To use it in the Command Line Interface (CLI), provide the PID identifying the service in the data type registry (for
example, `21.T11969/01370800d56a0d897dc1` is the identifier of the Cordra instance in the testbed) and run:

```shell
# Get information from the DOIP service
$ doipy hello '21.T11969/01370800d56a0d897dc1'

# List all available operations
$ doipy list_operations '21.T11969/01370800d56a0d897dc1'

# Search in the DOIP service for a DO
$ doipy search '21.T11969/01370800d56a0d897dc1' <query string> --username <username> --password <password>
```

To use it in the Python code simply import it and call the exposed methods. The return value of the methods is always of
type `<class 'dict'>`

```python
from doipy import hello, create
from pathlib import Path

# Call the hello operation
response = hello('21.T11969/01370800d56a0d897dc1')

# Call the create operation to create a DO
do_type = 'Document'
md = {'key1': 'value1', 'key2': 'value2'}
create(service='21.T11969/01370800d56a0d897dc1', do_type=do_type, bitsq=Path('file.txt'), metadata=md, password='', 
       client_id='')
```

### Create a Digital Object

To create a Digital Object (DO) in the CLI, first generate an input JSON file (called `input.json`) whose content
follows the below structure:

```json
{
  "file": "myDO_data.txt",
  "md-file": "myDO_md.json"
}
```

Here, `file` contains the bit-sequence of the DO and `md-file`contains metadata which are written into the PID record.
The `create` operation takes the file `input.json` and authentication credentials as input to build a DO. Simply run

```shell
$ doipy create input.json --client-id <client-id>
```

and provide the passwort when prompted.

### Create a FAIR Digital Object

To create a FAIR Digital Object (FDO) in the CLI, first generate an input JSON file (called `input.json`) whose content
follows the below structure:

```json
{
  "data-bit-sequences": [
    {
      "file": "myFDO_data_1.txt",
      "md-file": "myFDO_md_1.json"
    },
    {
      "file": "myFDO_data_2.txt",
      "md-file": "myFDO_md_2.json"
    }
  ],
  "metadata-bit-sequence": {
    "file": "myFDO_bundle_md.json",
    "md-file": "myFDO_bundle_md_md.json"
  }
}
```

The `create_fdo` command supports FDOs which consist of multiple data DOs and one metadata DO, following FDO
configuration type 4. The metadata DO describes the whole FDO as a bundle.

Each item in `data-bit-sequences` is a data bit-sequence `file` and its corresponding metadata `md-file`. One DO is
generated from each item in `data-bit-sequences`, with the `md-file` written into the PID record.
The `metadata-bit-sequence` corresponds to the DO that represents the metadata of the bundle FDO, with the `md-file`
written into the PID record of the metadata DO.

Use `create_fdo` to register an FDO with the data bit-sequences and metadata in the `input.json` file.

```shell
$ doipy '21.T11969/01370800d56a0d897dc1' create_fdo input.json --client-id <client-id>
```

and provide the passwort when prompted.

## For developer

The project is managed by [Poetry](https://python-poetry.org/). Therefore, make sure that Poetry is installed in your
system. Then run

```shell
$ poetry install
```

to install all dependencies. With this command, Poetry also installs the package in editable mode.
