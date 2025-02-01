# motorgo/cli.py
import glob
import os
import shutil
from pathlib import Path

import click
import questionary

# Global variables
# Path to PIO files
PIO_PATH = "~/.platformio"
RELATIVE_PLATFORM_PATH = "platforms"
RELATIVE_PACKAGES_PATH = "packages"

FRAMEWORK_NAME = "framework-arduinoespressif32"
PLATFORM_NAME = "espressif32"

BOARDS_TXT_PATH = "./platformio_board_defs/boards.txt"
BOARD_JSON_PATH = "platformio_tools/board_jsons/"
VARIANTS_PATH = "motorgo_experimental/variants/"


def copy_framework_files(
    framework_versioned_path: Path, variant_path: Path, force=False
):
    """
    Copy framework files to the specified versioned path.

    Args:
        framework_versioned_path (Path): The path to the versioned framework directory.
        variant_path (Path): The path to the variant to copy.
        force (bool): Whether to force overwrite existing files. Default is False.
    """

    # Define the path to the variants directory within the versioned framework directory
    variants_dir = framework_versioned_path / "variants"

    # Check if the variants directory exists
    if not variants_dir.exists():
        # Raise an error if the directory does not exist
        raise FileNotFoundError(f"Variants directory not found: {variants_dir}")

    try:
        # Attempt to copy the entire variant directory to the variants directory
        shutil.copytree(
            variant_path,
            variants_dir / variant_path.name,
        )
    except FileExistsError:
        if force:
            # If the force flag is set, notify the user that the variant will be overwritten
            click.secho(
                f"Overwriting variant {variant_path.name} in {variants_dir}.",
                fg="yellow",
            )

            # Remove the existing variant directory
            shutil.rmtree(variants_dir / variant_path.name)

            # Copy the variant directory again
            shutil.copytree(
                variant_path,
                variants_dir / variant_path.name,
            )
        else:
            # If the force flag is not set, notify the user that the variant already exists and will not be overwritten
            click.secho(
                f"Variant {variant_path.name} already exists in {variants_dir}. Use --force to overwrite.",
                fg="yellow",
            )
            return


def copy_platform_files(
    platform_versioned_path: Path, board_json_path: Path, force=False
):
    """
    Copy boards.json files to the specified versioned path.

    Args:
        platform_versioned_path (Path): The path to the versioned platform directory.
        board_json_path (Path): The path to the board json file to copy.
        force (bool): Whether to force overwrite existing files. Default is False.
    """

    # Path for platform boards
    boards_dir = os.path.join(platform_versioned_path, "boards")

    # Check if the boards directory exists
    if not os.path.exists(boards_dir):
        # Raise an error if the directory does not exist
        raise FileNotFoundError(f"Boards directory not found: {boards_dir}")

    try:
        # Attempt to copy the board JSON file to the boards directory
        shutil.copy2(
            board_json_path, os.path.join(boards_dir, os.path.basename(board_json_path))
        )
    except FileExistsError:
        if force:
            # If the force flag is set, notify the user that the board JSON file will be overwritten
            click.secho(
                f"Overwriting board JSON file {board_json_path} in {boards_dir}.",
                fg="yellow",
            )

            # Remove the existing board JSON file
            os.remove(os.path.join(boards_dir, os.path.basename(board_json_path)))

            # Copy the board JSON file again
            shutil.copy2(
                board_json_path,
                os.path.join(boards_dir, os.path.basename(board_json_path)),
            )
        else:
            # If the force flag is not set, notify the user that the board JSON file already exists and will not be overwritten
            click.secho(
                f"Board JSON file {board_json_path} already exists in {boards_dir}. Use --force to overwrite.",
                fg="yellow",
            )
            return


def get_platform_versions():
    """
    Retrieve the versions of installed platforms.

    This function scans the PlatformIO installation to find all installed versions of the platform definitions
    and returns a dictionary with the version as the key and the path as the value.

    Returns:
        dict: A dictionary where the keys are platform versions (str) and the
                values are the corresponding directory paths (str).

    Raises:
        FileNotFoundError: If the platforms_path does not exist.
        Exception: For any other unexpected errors during directory scanning.
    """

    # Get the path to the installed package
    platforms_path = Path(PIO_PATH).expanduser() / RELATIVE_PLATFORM_PATH

    # Check if the platforms_path exists
    if not platforms_path.exists():
        raise FileNotFoundError(f"Path not found: {platforms_path}")

    # Get list of all directories in platforms_path that match the pattern PLATFORM_NAME@* or PLATFORM_NAME
    platform_dirs = platforms_path.glob(f"{PLATFORM_NAME}@*")

    # Check if pattern PLATFORM_NAME exists:
    platform_dir_latest = platforms_path / PLATFORM_NAME
    if platform_dir_latest.exists():
        platform_dirs = [platform_dir_latest] + list(platform_dirs)

    platform_versions = {}

    # For each platform directory, get the version and add it to the dictionary
    for platform_dir in platform_dirs:
        if "@" in platform_dir.name:
            platform_version = platform_dir.name.split("@")[-1]
        else:
            platform_version = "latest"
        platform_versions[platform_version] = Path(platform_dir)

    return platform_versions


def get_framework_versions():
    """
    Retrieve the versions of installed frameworks.

    This function scans the PlatformIO installation to find all installed versions of the arduino-esp32
    framework and returns a dictionary with the version as the key and the path as the value.

    Returns:
        dict: A dictionary where the keys are framework versions (str) and the
              values are the corresponding directory paths (str).

    Raises:
        FileNotFoundError: If the frameworks_path does not exist.
        Exception: For any other unexpected errors during directory scanning.
    """

    # Get the path to the installed package
    frameworks_path = Path(PIO_PATH).expanduser() / RELATIVE_PACKAGES_PATH


    # Check if the frameworks_path exists
    if not frameworks_path.exists():
        raise FileNotFoundError(f"Path not found: {frameworks_path}")

    # Get list of all directories in frameworks_path that match the pattern FRAMEWORK_NAME OR FRAMEWORK_NAME@*
    framework_dirs = frameworks_path.glob(f"{FRAMEWORK_NAME}@*")

    # Check if pattern FRAMEWORK_NAME exists:
    framework_dir_latest = frameworks_path / FRAMEWORK_NAME
    if framework_dir_latest.exists():
        framework_dirs = [framework_dir_latest] + list(framework_dirs)

    framework_versions = {}

    # For each framework directory, get the version and add it to the dictionary
    for framework_dir in framework_dirs:
        if "@" in framework_dir.name:
            framework_version = framework_dir.name.split("@")[-1]
        else:
            framework_version = "latest"
        framework_versions[framework_version] = Path(framework_dir)

    return framework_versions


def install(all, force, board_name, board_path):
    """
    Install custom board definitions.
    """

    board_path = Path(board_path)

    # Search for the variant path using glob
    variant_path = board_path / VARIANTS_PATH / f"{board_name}"

    # Check if the variant and board JSON files exist
    if not variant_path.exists():
        click.secho(f"Variant path not found: {variant_path}", fg="red")
        click.secho(
            "This means that your board name is incorrect. If you're confident that the board name is correct, let Swapnil know.",
            fg="yellow",
        )
        return

    board_json_path = board_path / BOARD_JSON_PATH / f"{board_name}.json"

    if not board_json_path.exists():
        click.echo(f"Board JSON file not found: {board_json_path}")
        click.secho(
            "This probably means that Swapnil made a mistake - let him know.",
            fg="yellow",
        )
        return

    # Get the versions of the installed frameworks
    framework_versions = get_framework_versions()

    if not all:
        # Ask the user which versions to install the board definition to
        options = list(framework_versions.keys())

        if options:
            # Prompt the user to select a version
            versions = questionary.checkbox(
                "Select the framework version to install the board definition to:",
                choices=options,
            ).ask()

            if not versions:
                click.echo("No versions selected. Skipping framework installation.")
        else:
            click.echo("No framework versions found. Skipping framework installation. You may have to re-run this command after you try building your project.")
            versions = []

    else:
        versions = list(framework_versions.keys())

        if not versions:
            click.echo("No framework versions found. Exiting.")
            return

    # Copy the package files to the selected versions
    for version in versions:
        copy_framework_files(framework_versions[version], variant_path, force=force)

    # Get the versions of the installed platforms
    platform_versions = get_platform_versions()

    if not all:
        # Ask the user which versions to install the board definition to
        options = list(platform_versions.keys())

        # Prompt the user to select a version
        versions = questionary.checkbox(
            "Select the platform version to install the board definition to:",
            choices=options,
        ).ask()

        if not versions:
            click.echo("No versions selected. Exiting.")
            return

    else:
        versions = list(platform_versions.keys())

        if not versions:
            click.echo("No platform versions found. Exiting.")
            return

    # Copy the package files to the selected versions
    for version in versions:
        copy_platform_files(platform_versions[version], board_json_path, force=force)

    click.secho("\nBoard definition installed successfully.", fg="green", bold=True)
    click.secho(
        "\tNote: if you just installed a new version of the espressif32 platform in PlatformIO, you may have to run this command one more time after you try to build.",
        fg="yellow",
    )
