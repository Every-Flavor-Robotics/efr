import click
import os
import glob
import pathlib
from pathlib import Path
from plugins import plugin_template_utils
import requests
import pkg_resources

REGISTRY_URL = (
    "https://raw.githubusercontent.com/Every-Flavor-Robotics/efr/"
    "refs/heads/main/efr-plugins/efr-plugins/plugins/plugin_registry.json"
)



@click.group(name="plugins")
def plugins():
    """
    A 'plugins' command group for efr.
    """
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
    click.secho(f"\t4. Add the plugin to the registry using the `get_registry_info` command", fg="cyan")

    print(plugin_template_utils.get_github_raw_url(plugin_dir, Path("install.sh")))


@plugins.command(name = "get_registry_info")
@click.argument("plugin_dir", type=click.Path(exists=True))
def get_registry_info(plugin_dir: Path):
    plugin_dir = Path(plugin_dir)

    if not plugin_dir.exists():
        click.secho(f"Error: Directory '{plugin_dir}' does not exist.", fg="red")
        return


    plugin_name = plugin_dir.name.replace("efr-", "")
    plugin_description = plugin_template_utils.get_description(plugin_dir)
    plugin_install_url = plugin_template_utils.get_github_raw_url(plugin_dir, Path("install.sh"))

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
    try:
        response = requests.get(REGISTRY_URL)
        response.raise_for_status()
        registry = response.json()  # e.g., { "plugins": { "description": "...", "install_url": "..." } }
    except requests.RequestException as e:
        click.secho(f"Error fetching registry: {e}", fg="red")
        return

    # The registry might have multiple plugins keyed by name. Example structure:
    #
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
    # But your example shows only a top-level "plugins" key. Adjust as needed.
    #
    # For the example:
    # {
    #   "plugins": {
    #       "description": "...",
    #       "install_url": "..."
    #   }
    # }
    # We'll assume each top-level key is a plugin name. The user’s example is somewhat ambiguous,
    # so adapt to your real JSON structure.

    # If your real structure has a single key "plugins" for one plugin, do something like:
    #   plugin_data = registry["plugins"]
    #   plugin_name = "plugins"
    #   # Then wrap that in a dict so it matches { plugin_name: plugin_data }
    #
    # If your real structure is multiple named plugins, you can iterate them directly.
    # Example below handles both cases gracefully.

    if "plugins" in registry and isinstance(registry["plugins"], dict):
        # The example shows only one plugin named "plugins"
        # We'll treat that as { "plugins": {...} } => one plugin named "plugins"
        # but let's unify it into a dictionary of { "plugins": { ... } }
        # so we can iterate the same way if you had multiple.
        plugin_registry = {"plugins": registry["plugins"]}
    else:
        # Otherwise, we assume the entire JSON is a map of plugin_name -> plugin_info
        plugin_registry = registry

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
            click.secho(f"   Install URL: {url}", fg="cyan")
    else:
        click.echo("(No uninstalled plugins found)")

    click.echo()



