# motorgo/cli.py
import click
from pathlib import Path
from motorgo import board_install
import requests
import tempfile
import subprocess

EXPERIMENTAL_BOARDS_REPO = (
    "https://github.com/Every-Flavor-Robotics/motorgo-experimental-boards/"
)


def get_available_boards():
    PACKAGE_INDEX_PATH = "https://raw.githubusercontent.com/Every-Flavor-Robotics/motorgo-experimental-boards/refs/heads/main/efr_board_index.json"
    try:
        # Get the list of available boards from the package index
        package_index = requests.get(PACKAGE_INDEX_PATH).json()
        boards = package_index["boards"]
        return boards
    except Exception as e:
        return None


@click.group(
    name="motorgo",
    invoke_without_command=True,
    help="""
Tools for managing MotorGo hardware and software development.

Software development tools:\n
    boards       Tools for interacting with custom board definitions
""",
)
@click.pass_context
def motorgo(ctx):
    """
    A 'motorgo' command group for efr.
    """
    if ctx.invoked_subcommand is None:
        click.secho("⚙️  efr motorgo  ⚙️", fg="green", bold=True)
        click.echo()

        click.secho(
            "The motorgo plugin provides tools for managing MotorGo hardware and software development.\n    ",
            fg="cyan",
        )

        click.secho("List of software dev commands:", fg="cyan", bold=True)
        click.secho(
            "  boards               Tools for interacting with custom board definitions",
            fg="yellow",
        )

        click.echo()
        click.secho("Examples:", fg="cyan", bold=True)
        click.echo("  efr motorgo boards install --help")
        click.echo("  efr motorgo boards list")

        click.echo()
        click.echo(
            "Use 'Invoke any subcommand with --help for more details on usage.\n"
        )
        click.secho("Happy MotorGo hacking!", fg="magenta", bold=True)

        # Exit so Click doesn't complain about missing subcommands
        ctx.exit(0)


@motorgo.group(invoke_without_command=True)
@click.pass_context
def boards(ctx):
    """
    Tools for interacting with experimental board definitions.
    """
    if ctx.invoked_subcommand is None:
        # Print your docstring/info in a colorful, emoji-decorated format
        click.secho(
            "Tools for working with experimental board definitions.\n",
            fg="green",
            bold=True,
        )

        click.secho(
            "To check if a board is experimental or production, refer to the docs at: https://docs.motorgo.net/standalone_mode/board_setup\n",
            fg="cyan",
        )

        click.secho("Available Commands:", fg="cyan", bold=True)
        click.secho(
            "\tinstall\t\tInstall custom board definitions for PlatformIO", fg="yellow"
        )
        click.secho("\tuninstall\tActually does nothing :)", fg="yellow")
        click.secho(
            "\tlist\t\tPrints the available boards, and their identifiers for installing",
            fg="yellow",
        )

        print()
        click.secho("Available Boards:", fg="cyan", bold=True)
        boards = get_available_boards()
        if boards:
            for board in boards:
                click.secho(f"\t{board['name']}: {board['identifier']}", fg="yellow")
        else:
            click.secho("\tError fetching board list", fg="red")

        # click.secho(
        #     "If you're not sure which versions of the platform and framework to install to, "
        #     "you can use the --all flag to install to all available platforms and frameworks. "
        #     "This is generally safe! \U0001F680\n",  # Rocket emoji
        #     fg="yellow",
        # )

        # Exit after showing this info so that Click doesn't complain about a missing subcommand
        ctx.exit(0)


@boards.command(
    name="list",
    help="Prints the available boards, and their identifiers for installing.",
)
def list():
    boards = get_available_boards()
    if boards:
        for board in boards:
            click.secho(f"{board['name']}: {board['identifier']}", fg="yellow")
    else:
        click.secho("Error fetching board list", fg="red")


@boards.command(
    name="install",
    help="""
Installs custom board definition for PlatformIO.

If you don't know which versions of the platform and framework to install to, you can use the --all flag to install to all available platforms and frameworks. This is generally safe!
""",
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
    "--custom-board-path",
    required=False,
    type=click.Path(exists=True),
    help="Pass a custom path for the experimental boards repo, for development purposes.",
)
def install(all, force, board_name, custom_board_path):
    """
    Install custom board definitions.
    """

    click.secho(f"Installing board '{board_name}'...", fg="green")

    boards = get_available_boards()
    # Confirm that the board exists
    board_exists = False
    for board in boards:
        if board["identifier"] == board_name:
            board_exists = True
            break

    if not board_exists:
        click.secho(
            f"Board '{board_name}' not found in the list of available boards.", fg="red"
        )
        click.secho(
            "Run 'efr motorgo boards list' to see the list of available boards.",
            fg="yellow",
        )
        return

    temp_dir = None
    if not custom_board_path:
        # Clone the repo to a temporary directory
        temp_dir = tempfile.TemporaryDirectory()
        custom_board_path = Path(temp_dir.name)

        try:
            subprocess.run(
                ["git", "clone", EXPERIMENTAL_BOARDS_REPO, custom_board_path],
                stdout=subprocess.DEVNULL,  # Suppress standard output
                stderr=subprocess.DEVNULL,  # Suppress error output
                check=True,  # Raise an exception if git fails
            )
        except subprocess.CalledProcessError:
            print(
                f"Error: Failed to clone repository {EXPERIMENTAL_BOARDS_REPO} into {custom_board_path}"
            )

    board_install.install(all, force, board_name, custom_board_path)

    if temp_dir:
        temp_dir.cleanup()


@boards.command(name="uninstall", help="")
def uninstall():
    pass
