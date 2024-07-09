""" Setup PIP and Poetry for publishing to Nexus and using Nexus as the primery source """

import os
import subprocess
from .pip_config import setup_pypi, read_credentials


def configure_python_for_nexus(**kwargs):
    """Configure Python to publish to Nexus"""

    repo_name = kwargs.get("name", "nexus")

    print("Configuring Python to publish to Nexus")

    environment = os.environ.copy()

    # Upgrade pip to the latest version
    subprocess.run(
        ["python", "-m", "pip", "install", "--upgrade", "pip"],
        env=environment,
        check=True,
    )

    # Write the .pypirc file and the ~/.config/pip/pip.conf file
    setup_pypi(**kwargs)

    # List the configuration
    subprocess.run(["pip", "config", "list"], env=environment, check=True)

    # Install all the dependencies this project needs
    subprocess.run(
        ["pip", "install", "poetry", "poetry-dynamic-versioning"],
        env=environment,
        check=True,
    )
    subprocess.run(["pip", "install", "pyinstaller"], env=environment, check=True)

    print(
        'Add the Nexus repository to the list of poetry sources as the "primary" source'
    )
    nexus_server, repository, nexus_username, nexus_password = read_credentials(
        "credentials-read", **kwargs
    )

    # Password for our 'nexus' server
    subprocess.run(
        ["poetry", "config", f"http-basic.{repo_name}", nexus_username, nexus_password],
        env=environment,
        check=True,
    )

    subprocess.run(
        [
            "poetry",
            "source",
            "add",
            "--priority=primary",
            repo_name,
            f"{nexus_server}{repository}/simple/",
        ],
        env=environment,
        check=True,
    )
    subprocess.run(
        ["poetry", "source", "add", "--priority=explicit", "PyPI"],
        env=environment,
        check=True,
    )

    print('Add a publishing location with "poetry publish --repository nexus-releases"')
    nexus_server, repository, nexus_username, nexus_password = read_credentials(
        "credentials-write", **kwargs
    )

    subprocess.run(
        [
            "poetry",
            "config",
            f"repositories.{repo_name}-releases",
            f"{nexus_server}{repository}/",
        ],
        env=environment,
        check=True,
    )
    subprocess.run(
        [
            "poetry",
            "config",
            f"http-basic.{repo_name}-releases",
            nexus_username,
            nexus_password,
        ],
        env=environment,
        check=True,
    )

    subprocess.run(["poetry", "update"], env=environment, check=True)
    subprocess.run(["poetry", "install", "--all-extras"], env=environment, check=True)
