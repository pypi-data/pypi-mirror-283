import click
import os
import getpass
from docker_shell import DockerShell

def create_docker_container():
    """
    Creates a Docker container for running commands on Thunder in MacOS and Windows. If you are having trouble in your linux environment, this command may help.
    """

    ports = [8888, 8001]
    args = [
        '-u',
        'root',
        # 'thunder'
        # '--privileged'
    ]
    for port in ports:
        args.extend(['-p', str(port)])

    try:
        msg = "Launching thunder container and forwarding the following ports:"
        for port in ports:
            msg += f'\n  - {port}'
        click.echo(click.style(msg, fg='blue', bold=True))
        DockerShell(image='thundercompute/thunder:latest', shell='zsh', dockerArgs=args).launch()
    except Exception as _:
        click.echo(click.style("Failed to launch docker container! Please make sure that docker is installed and the daemon is running.", bg='red', fg='white', bold=True))
