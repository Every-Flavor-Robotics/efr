# motorgo/cli.py
import click
import os
import glob
from pathlib import Path
from motorgo import board_install


@click.group(name="motorgo")
def motorgo():
    """
    A 'motorgo' command group for efr.
    """
    pass


@motorgo.group()
def boards():
    """
    Tools for interacting with custom board definitions.
    """
    pass


@boards.command()
@click.option(
    "-a",
    "--all",
    is_flag=True,
    help="Install the custom board definition to all installed esp-arduino frameworks and platforms.",
)
@click.option(
    "--force",
    is_flag=True,
    help="Force overwrite of existing custom board installations.",
)
@click.option(
    "--board-name",
    required=True,
    type=click.STRING,
    help="Name of the board to install. Example: 'motorgo_plink'",
)
@click.option(
    "--framework-path",
    required=True,
    type=click.Path(exists=True),
    help="Path to the framework where the board will be installed.",
)
@click.option(
    "--platform-path",
    required=True,
    type=click.Path(exists=True),
    help="Path to the platform definitions directory.",
)
def install(all, force, board_name, framework_path, platform_path):
    """
    Install custom board definitions.
    """

    board_install.install(all, force, board_name, framework_path, platform_path)