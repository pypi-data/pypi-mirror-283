# Build Tools

## Description
Tools to help you setup your python project to interact with the NEXUS server and
provide other standard files.
## Installation
To use this tool, install it with PIP.
```shell
pip install simple-build-tools
```
The latest version is Version 0.1.2
## Usage
Once you have it installed, a script **bt** will be available to run on the command line in your Python environment, you can run one of the three commands:
```shell
bt -h
usage: bt [-h] {nexus,flake8,gitignore}

Tools to setup environment for Python Nexus

positional arguments:
  {nexus,flake8,gitignore}
                        nexus: Setup project to use Nexus is PyPi source
                        flake8: Add a .flake8 config file to the project folder
                        gitignore: Add a stndard gitignore to thep roject folder

options:
  -h, --help            show this help message and exit
```
**Command: bt nexus**
Setup the pip and poetry environment on your project to use the NEXUS server.

This requires either a "credentials.ini" file in the current folder, or environment varialbes.

**credentials.ini**
```ini
[credentials-read]
host = nexus.yourdomain.com
repository = /repository/pypi
username = <your username>
password = <your password or access token>

[credentials-write]
host = nexus.yourdomain.com
repository = /repository/pypi-releases
username = <your username>
password = <your password>
```

Alternatively, you may have the enviroment variables already defined:

```shell
NEXUS_SERVER="https://nexus.yourdomain.com"
NEXUS_USERNAME="<your username>"
NEXUS_PASSWORD="<your password or teken"
```

**Command:  bt flake8**
Writes a basic **.flake8** configuration file in your project folder.  It will overwrite your existing file if you say "Yes" to the prompt.

**Command:  bt gitignore**
Writes a comprehensive **.gitignore** file in your project folder.  It will overwrite your existing file if yo say "Yes" to the prompt.

## Contributing
Guidelines for contributing to the project.

None:  Have at it.

## License
MIT

Take it, it's yours
