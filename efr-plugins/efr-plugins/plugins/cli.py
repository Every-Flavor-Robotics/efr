import click
import os
import glob
import pathlib
from pathlib import Path
from plugins import plugin_template_utils


@click.group(name="plugins")
def plugins():
    """
    A 'plugins' command group for efr.
    """
    pass


@plugins.command(name = "list")
def list_available_plugins():
    pass


@plugins.command(name = "init")
@click.argument("name")
@click.option("--path", default=os.getcwd(), help="Path to create the new plugin project")
def init_new_plugin(name: str, path: Path):
    path = Path(path)

    # Confirm the target directory exists
    # Print error in red
    if not path.exists():
        click.secho(f"Error: Directory '{path}' does not exist.", fg="red")
        return

    # Questionary to ask for a description
    description = click.prompt("Enter a short description for your plugin")

    plugin_dir = plugin_template_utils.create_new_plugin_project(path, name)

    plugin_template_utils.init_readme(plugin_dir, name, description)
    plugin_template_utils.init_setup_py(plugin_dir, name, description)
    plugin_template_utils.init_cli_py(plugin_dir, name, description)






