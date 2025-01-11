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


@boards.command(
    name="install",
    help="""
Installs custom board definition for PlatformIO.

To get started, clone the two repositories below to your local machine:\n
\t- Arduino-ESP32 Framework: https://github.com/Every-Flavor-Robotics/arduino-esp32.git\n
\t- Espressif32 Platform: https://github.com/Every-Flavor-Robotics/platform-espressif32.git

Pass those paths to the install command utility as shown below.\n
If you're not sure which of the platform and framework to install to, you can use the --all flag to install to all available platforms and frameworks. This is generall safe!

"""
)
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

@boards.command(
    name="uninstall",
    help="")
def uninstall():
    pass