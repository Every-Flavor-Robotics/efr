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


@motorgo.group(invoke_without_command=True)
@click.pass_context
def boards(ctx):
    """
    Tools for interacting with custom board definitions.
    """
    if ctx.invoked_subcommand is None:
        # Print your docstring/info in a colorful, emoji-decorated format
        click.secho("Installs custom board definition for PlatformIO.\n", fg="green", bold=True)

        click.secho(
            "To get started, clone the two repositories below to your local machine:",
            fg="cyan",
        )
        click.echo("\t• Arduino-ESP32 Framework: https://github.com/Every-Flavor-Robotics/arduino-esp32.git")
        click.echo("\t• Espressif32 Platform:     https://github.com/Every-Flavor-Robotics/platform-espressif32.git\n")

        click.secho(
            "Pass those paths to the install command utility as shown below.", fg="yellow")
        click.secho(
                        "\tefr motorgo boards install --board-name <board_name> --framework-path <path_to_framework> --platform-path <path_to_platform>\n\n"

        )
        click.secho(
            "If you're not sure which of the platform and framework to install to, "
            "you can use the --all flag to install to all available platforms and frameworks. "
            "This is generally safe! \U0001F680\n",  # Rocket emoji
            fg="yellow",
        )

        # Exit after showing this info so that Click doesn't complain about a missing subcommand
        ctx.exit(0)


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