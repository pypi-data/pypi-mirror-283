""" Write the configuration for PIP and Poetry to use Nexus as the primary source """

import configparser
import os
import subprocess
from typing import Optional, Tuple
from urllib.parse import urlparse


def add_host_to_pypirc(section_name, host, repository, username, password):
    """
    Add to pypirc file.  Make sure that repository starts with /.  You have to add it
    so you can add a port.

    do NOT put the port on the "host" variable

    ex.
        host = pypi.org
        repository = :9091/repository/pypi-group
        repository = /repository/pypi-release

    :param section_name:
    :param host:
    :param repository:
    :param username:
    :param password:
    :return:
    """

    repository = repository.rstrip("/")

    # Read the existing .pypirc file
    # Define the path to the .pypirc file
    home_folder = os.path.expanduser("~")
    pypirc_file = os.path.join(home_folder, ".pypirc")
    config = configparser.ConfigParser()
    config.read(pypirc_file)

    # Update or add the sections and options as needed
    if section_name not in config:
        config.add_section(section_name)

    config.set(section_name, "repository", f"{host}{repository}/")
    if not username and config.has_option(section_name, "username"):
        config.remove_option(section_name, "username")
    else:
        config.set(section_name, "username", username)
    if not password and config.has_option(section_name, "password"):
        config.remove_option(section_name, "password")
    else:
        config.set(section_name, "password", password)

    if "distutils" not in config:
        config.add_section("distutils")
    if config.has_option("distutils", "index-servers"):
        indexes = config.get("distutils", "index-servers")
    else:
        indexes = ""
    if section_name not in indexes:
        if indexes:
            indexes = indexes + "\n"
        indexes = indexes + section_name
        config.set("distutils", "index-servers", indexes)

    # Save the updated .pypirc file
    with open(pypirc_file, "w") as configfile:
        config.write(configfile)


def add_to_gitignore():
    # Read the credentials from the external file (credentials.ini)
    # Please do NOT commit this to your repository!

    # Define the file to check and the line to add
    file_to_check = ".gitignore"
    line_to_add = "credentials.ini\n"

    # Check if the line is already in the file
    if not os.path.isfile(file_to_check):
        with open(file_to_check, "w") as gitignore_file:
            gitignore_file.write(line_to_add)
    else:
        with open(file_to_check, "r") as gitignore_file:
            lines = gitignore_file.readlines()

        if line_to_add not in lines:
            with open(file_to_check, "a") as gitignore_file:
                gitignore_file.write(line_to_add)


def split_url(url) -> Tuple[str, str, str, str]:
    """return a tuple of this url split apart"""
    parsed_url = urlparse(url)

    protocol = parsed_url.scheme
    host = parsed_url.hostname
    port = str(parsed_url.port)
    path = parsed_url.path

    return protocol, host, port, path


def input_host(prompt: str):
    """ test the input to ensure it's a URL"""
    while True:
        host = input(prompt)
        protocol, host, port, _ = split_url(host)
        if not host:
            print("You must enter a hostname")
        if not protocol or (protocol != "http://" and protocol != "https://"):
            print("You have to enter http://... or https://...")
        if protocol and host:
            break
    host = f"{protocol}://{host}"
    if port:
        host = f"{host}:{port}"
    return host


def read_credentials_input():

    while True:
        host = input_host("Host (Ex. http://example.com:8000): ")
        repository = input("Repository: ")
        username = input("Username: ")
        password = input("Password: ")

        print("The values you have entered are:")
        print(f"Host: {host}")
        print(f"Repository: {repository}")
        print(f"Username: {username}")
        print(f"Password: {password}")
        print()
        confirm = input("Confirm: [y/N]:")
        if confirm.lower() == "y":
            return host, repository, username, password


def check_host(hostname: str):
    if not hostname.startswith("https://") and not hostname.startswith("http://"):
        return f"https://{hostname}"
    else:
        return hostname


def get_if(config, section, option, default_value: Optional[str] = None):
    rv = None
    if config.has_option(section, option):
        rv = config.get(section, option)
    return rv if rv else default_value


def read_credentials_file(section, **kwargs):
    """read credentials from the ini file"""
    if os.path.exists("credentials.ini"):
        credentials_config = configparser.ConfigParser()
        credentials_config.read("credentials.ini")
        if credentials_config.has_section(section):
            host = get_if(credentials_config, section, "host")
            if host:
                repository = get_if(credentials_config, section, "repository")
                username = get_if(credentials_config, section, "username")
                password = get_if(credentials_config, section, "password")
                return check_host(host), repository, username, password

    return None, None, None, None


def read_credentials_env():
    """read credentials from the environment variables"""
    host = check_host(os.getenv("NEXUS_SREVER", None))
    if host:
        username = os.getenv("NEXUS_USERNAME", None)
        password = os.getenv("NEXUS_PASSWORD", None)
        repository = "/repository/pypi"
        return check_host(host), repository, username, password

    return None, None, None, None

def read_credentials_commandline(**kwargs):
    host = kwargs.get("nexus_url", None)
    if host:
        repository = "/repository/pypi"
        password = kwargs.get("nexus_password", None)
        username = kwargs.get("nexus_username", None)
        return check_host(host), repository, username, password

    return None, None, None, None

def read_credentials(section, **kwargs):

    print(f"Reading credentials for [{section}]")

    # First try to get the information from the command line arguments
    host, repository, username, password = read_credentials_commandline(**kwargs)

    # If we don't get the information from command line, then try the ini file
    if not host:
        host, repository, username, password = read_credentials_file(section)

    # If we don't get the information from the command line or ini file, then try environment variables
    if not host:
        host, repository, username, password = read_credentials_env()

    # If we still don't have the details, then ask the user for them
    if not host:
        host, repository, username, password = read_credentials_input()

    return host, repository, username, password


def update_pip_ini(name, host, repository):
    """
    Sets the INDEX URL in pip.ini so that it points to the specified repository and can
    read python packages from there.

    :param section: set to "global" to use the global section of pip.ini.
    :param host:
    :param repository:
    :return:
    """

    repository = repository.rstrip("/")
    if repository.endswith("/simple"):
        repository = repository[:-7]
    index_url = f"{host}{repository}"

    _, server, port, _ = split_url(host)
    if port:
        server = f"{server}:{port}"

    commands = [
        f'pip config --user set {name}.index "{index_url}/"',
        f'pip config --user set {name}.index-url "{index_url}/simple/"',
        f'pip config --user set {name}.trusted-host "{server}"',
    ]

    for command in commands:
        subprocess.run(command, shell=True, check=True)


def setup_pypi(**kwargs):

    repo_name = kwargs.get("name", "pypi")

    host, repository, username, password = read_credentials(
        "credentials-read", **kwargs
    )

    add_host_to_pypirc(
        repo_name,
        host,
        repository,
        username,
        password
    )

    update_pip_ini(repo_name, host, repository)

    # Special, Update the "global" section of the pip ini
    update_pip_ini("global", host, repository)

    repo_name = f"{repo_name}-publish"

    host, repository, username, password = read_credentials(
        "credentials-write", **kwargs
    )

    add_host_to_pypirc(
        repo_name,
        host,
        repository,
        username,
        password
    )

    update_pip_ini(repo_name, host, repository)
