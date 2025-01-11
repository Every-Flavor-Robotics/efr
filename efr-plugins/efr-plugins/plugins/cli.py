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
    description = click.prompt("Enter a short description for your plugin (e.g. 'A plugin for managing awesome things.')")

    try:
        plugin_dir = plugin_template_utils.create_new_plugin_project(path, name)
    except FileExistsError:
        click.secho(f"Error: Directory 'efr-{name}' already exists in '{path}'.", fg="red")
        return

    plugin_template_utils.init_readme(plugin_dir, name, description)
    plugin_template_utils.init_setup_py(plugin_dir, name, description)
    plugin_template_utils.init_cli_py(plugin_dir, name, description)
    plugin_template_utils.init_install_sh(plugin_dir, name)

    # Print a checklist for what the user should do next
    click.secho(f"\nPlugin '{name}' initialized at: {plugin_dir.resolve()}\n", fg="green")
    click.secho("Next steps:", fg="cyan")
    click.secho(f"\t1. Add info to setup.py", fg="cyan")
    click.secho(f"\t2. Implement your plugin in cli.py", fg="cyan")
    click.secho(f"\t3. Update README.md with details", fg="cyan")






