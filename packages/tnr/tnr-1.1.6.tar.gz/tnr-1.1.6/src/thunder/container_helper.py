import subprocess
import click
import os
import getpass
from docker_shell import DockerShell
import docker


def create_docker_container():
    """
    Creates a Docker container for running commands on Thunder in MacOS and Windows. If you are having trouble in your linux environment, this command may help.
    """

    ports = [8888, 8001]
    args = [
        "-u",
        "root",
        # 'thunder'
        # '--privileged'
    ]
    for port in ports:
        args.extend(["-p", str(port)])

    try:
        msg = "Launching thunder container and forwarding the following ports:"
        for port in ports:
            msg += f"\n  - {port}"
        click.echo(click.style(msg, fg="blue", bold=True))

        image = "thundercompute/thunder:latest"
        # if shell.requiresPull(image) == True:
        #     click.echo("unable to find image locally")
        #     shell.pull(image)
        shell = DockerShell(image, shell="zsh", dockerArgs=args)

        if shell.requiresPull():
            shell.pull()

        shell.launch()

    except Exception as e:
        click.echo(
            click.style(
                f"Failed to launch docker container! Please make sure that docker is installed and the daemon is running: {e}.",
                bg="red",
                fg="white",
                bold=True,
            )
        )
