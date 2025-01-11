import click
import os
import glob
import pathlib
from pathlib import Path
from plugins import plugin_utils
import subprocess
import pkg_resources
import requests


@click.group(
    name="plugins",
    invoke_without_command=True,
    help="""
Utilities for installing plugins for the `efr` CLI and for developing new plugins.\n

  list                 List available plugins from the plugin registry.
  install <plugin>     Install a plugin by name.
  uninstall <plugin>   Uninstall a plugin by name.

For development:\n
  init                 Initialize a new plugin project, filling in boilerplate.
  get_registry_info    Get registry info for a plugin project to paste into the registry.
""",
)
@click.pass_context
def plugins(ctx):
    """
    A 'plugins' command group for efr.
    """
    if ctx.invoked_subcommand is None:
        click.secho("🔌  efr plugins  🔌", fg="magenta", bold=True)
        click.echo()
        click.secho("List of commands:", fg="cyan", bold=True)
        click.secho("  list                 List available plugins from the plugin registry", fg="yellow")
        click.secho("  install <plugin>     Install a plugin by name", fg="yellow")
        click.secho("  uninstall <plugin>   Uninstall a plugin by name", fg="yellow")

        click.echo()
        click.secho("For development:", fg="cyan", bold=True)

        click.secho("  init                 Initialize a new plugin project. This sets up the plugin project fully", fg="yellow")
        click.secho("  get_registry_info    Get registry info for a plugin project", fg="yellow")

        click.echo()
        # Documentation link
        click.echo(
            "\nFor more details on creating and installing plugins, see:\n"
            "  https://github.com/Every-Flavor-Robotics/efr/blob/main/plugin_docs.md"
        )

        # Exit so Click doesn't complain about missing subcommands
        ctx.exit(0)




@plugins.command(name = "init",
help="Initialize a new plugin project, filling in boilerplate.")
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
        plugin_dir = plugin_utils.create_new_plugin_project(path, name)
    except FileExistsError:
        click.secho(f"Error: Directory 'efr-{name}' already exists in '{path}'.", fg="red")
        return

    plugin_utils.init_readme(plugin_dir, name, description)
    plugin_utils.init_setup_py(plugin_dir, name, description)
    plugin_utils.init_cli_py(plugin_dir, name, description)
    plugin_utils.init_install_sh(plugin_dir, name)

    # Print a checklist for what the user should do next
    click.secho(f"\nPlugin '{name}' initialized at: {plugin_dir.resolve()}\n", fg="green")
    click.secho("Next steps:", fg="cyan")
    click.secho(f"\t1. Add info to setup.py", fg="cyan")
    click.secho(f"\t2. Implement your plugin in cli.py", fg="cyan")
    click.secho(f"\t3. Update README.md with details", fg="cyan")
    click.secho(f"\t4. Add the plugin to the registry using the `get_registry_info` command", fg="cyan")

    print(plugin_utils.get_github_raw_url(plugin_dir, Path("install.sh")))


@plugins.command(name = "get_registry_info",
help="Get registry info for a new plugin to add it to the plugin registry.")
@click.argument("plugin_dir", type=click.Path(exists=True))
def get_registry_info(plugin_dir: Path):
    plugin_dir = Path(plugin_dir)

    if not plugin_dir.exists():
        click.secho(f"Error: Directory '{plugin_dir}' does not exist.", fg="red")
        return


    plugin_name = plugin_dir.name.replace("efr-", "")
    plugin_description = plugin_utils.get_description(plugin_dir)
    plugin_install_url = plugin_utils.get_github_raw_url(plugin_dir, Path("install.sh"))

    print(plugin_description)

    # Provide JSON output for the registry
    click.secho(f"Add the following to the registry in 'efr-plugins':", fg="green")
    click.secho(f"\"{plugin_name}\": {{", fg="cyan")
    click.secho(f"\t\"description\": \"{plugin_description}\",", fg="cyan")
    click.secho(f"\t\"install_url\": \"{plugin_install_url}\"", fg="cyan")
    click.secho(f"}},", fg="cyan")





@plugins.command(name="list")
def list_plugins():
    """
    List available plugins from the registry, showing which are installed vs. not installed.
    """

    click.secho("Fetching plugin registry...", fg="cyan")
    plugin_registry = plugin_utils.retrieve_registry()

    # Registry structure is assumed to be a dictionary like:
    # {
    #    "plugin_a": {
    #       "description": "...",
    #       "install_url": "..."
    #    },
    #    "plugin_b": {
    #       "description": "...",
    #       "install_url": "..."
    #    }
    # }
    #
    # We'll assume each top-level key is a plugin name. The user’s example is somewhat ambiguous,
    # so adapt to your real JSON structure.

    # Gather installed package names (lowercased) for easy membership checking
    installed_packages = {dist.project_name.lower() for dist in pkg_resources.working_set}

    installed_list = []
    uninstalled_list = []

    # Each key in plugin_registry is a plugin name (e.g. "plugins", "motor-go", "foo", etc.)
    for plugin_name, plugin_info in plugin_registry.items():
        # By convention, we might expect the installed package to be "efr-<plugin_name>"
        # or some other known naming scheme. Adjust as necessary:
        pkg_name = f"efr-{plugin_name}".lower()

        if pkg_name in installed_packages:
            installed_list.append((plugin_name, plugin_info))
        else:
            uninstalled_list.append((plugin_name, plugin_info))

    click.secho("\n==== INSTALLED PLUGINS ====", fg="green")
    if installed_list:
        for name, info in installed_list:
            desc = info.get("description", "No description")
            click.echo(f"• {name} : {desc}")
    else:
        click.echo("(No plugins installed)")

    click.secho("\n==== UNINSTALLED PLUGINS ====", fg="yellow")
    if uninstalled_list:
        for name, info in uninstalled_list:
            desc = info.get("description", "No description")
            url = info.get("install_url", "No install URL provided")
            click.echo(f"• {name} : {desc}")
    else:
        click.echo("(No uninstalled plugins found)")

    click.echo()


@plugins.command(name="install")
@click.argument("plugin_name")
@click.option(
    "--upgrade",
    is_flag=True,
    default=False,
    help="Re-install or upgrade the plugin even if it's already installed."
)
def install_plugin(plugin_name, upgrade):
    """
    Install a plugin by name, using its install script from the registry.
    Does nothing if already installed (unless --upgrade is specified).
    """

    # 1) Get the plugin registry
    registry = plugin_utils.retrieve_registry()  # e.g., returns dict from plugin_registry.json

    # Check if the plugin is in the registry
    plugin_info = registry.get(plugin_name)
    if not plugin_info:
        click.secho(f"Plugin '{plugin_name}' not found in registry.", fg="red")
        return

    install_url = plugin_info.get("install_url")
    if not install_url:
        click.secho(f"Plugin '{plugin_name}' has no install_url in registry.", fg="red")
        return

    # 2) Check if plugin is already installed
    already_installed = plugin_utils.is_plugin_installed(plugin_name)

    if already_installed and not upgrade:
        click.secho(f"'{plugin_name}' is already installed. Use --upgrade to force re-install.", fg="yellow")
        return

    # 3) Pull down the install script
    try:
        click.secho(f"Fetching install script from {install_url} ...", fg="cyan")
        resp = requests.get(install_url)
        resp.raise_for_status()
    except requests.RequestException as e:
        click.secho(f"Error downloading install script: {e}", fg="red")
        return

    # 4) Write the script to a temporary file
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".sh") as tmp_file:
        script_path = tmp_file.name
        tmp_file.write(resp.text)

    click.secho(f"Running install script for '{plugin_name}' ...", fg="cyan")
    try:
        # 5) Run the script
        subprocess.run(["bash", script_path], check=True)
        click.secho(f"'{plugin_name}' installed (or upgraded) successfully!", fg="green")
    except subprocess.CalledProcessError as e:
        click.secho(f"Error running install script: {e}", fg="red")
    finally:
        # 6) Cleanup: remove the temporary script
        if os.path.exists(script_path):
            os.remove(script_path)


@plugins.command(name="uninstall")
@click.argument("plugin_name")
def uninstall_plugin(plugin_name):
    """
    Uninstall a plugin by name, using pip.
    """

    if not plugin_utils.is_plugin_installed(plugin_name):
        click.secho(f"Plugin '{plugin_name}' is not installed.", fg="yellow")
        return

    # By convention, the package is 'efr-<plugin_name>'
    package_name = f"efr-{plugin_name}"

    click.secho(f"Uninstalling '{package_name}'...", fg="cyan")
    try:
        subprocess.run(
            ["pip", "uninstall", "-y", package_name],  # -y to skip confirmation
            check=True
        )
        click.secho(f"'{plugin_name}' successfully uninstalled!", fg="green")
    except subprocess.CalledProcessError as e:
        click.secho(f"Failed to uninstall '{plugin_name}': {e}", fg="red")