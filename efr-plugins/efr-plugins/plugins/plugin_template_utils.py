import os
from pathlib import Path
import click

def create_new_plugin_project(path: Path, name: str):
    """
    Create a skeleton directory structure for a new efr plugin project.

    This function generates:
      1. A main directory named efr-<name>.
      2. A Python package directory matching 'name'.
      3. Touch setup.py, __init__.py, and cli.py in the package.
      4. A README.md for project documentation.
      5. An __init__.py and cli.py in the package.

    Args:
        path (Path): The parent directory where the new plugin project will be created.
        name (str): The plugin name. For example, if name="awesome", the project folder will be efr-awesome
                    and the Python package will be named "awesome".
    Returns:
        plugin_dir (Path): The full path to the new plugin directory.
    Raises:
        FileExistsError: If the target plugin directory already exists.
    """

    # 1) Construct full path for the new plugin directory: efr-<plugin_name>
    plugin_dir_name = f"efr-{name}"
    plugin_dir = path / plugin_dir_name

    if plugin_dir.exists():
        raise FileExistsError(f"Directory '{plugin_dir}' already exists. Aborting to avoid overwriting.")

    # Create the top-level plugin directory
    plugin_dir.mkdir(parents=True, exist_ok=False)

    # 2) Create the Python package folder matching 'name'
    #    e.g., efr-awesome/awesome/
    package_dir = plugin_dir / name
    package_dir.mkdir(parents=True, exist_ok=False)

    # 3) Create __init__.py
    init_file = package_dir / "__init__.py"
    init_file.touch()

    # 4) Create cli.py
    cli_file = package_dir / "cli.py"
    cli_file.touch()

    # 5) Create setup.py
    setup_file = plugin_dir / "setup.py"
    setup_file.touch()

    # 6) Create README.md
    readme_file = plugin_dir / "README.md"
    readme_file.touch()

    return plugin_dir



def _init_file(template_path: str, target_path: Path, name: str, description: str):
    """
    Initialize a file from the templates folder for the new efr plugin project.

    This function:
      1. Reads the template file from the local 'templates' folder.
      2. Substitutes placeholders (e.g., '{name}' '{description}') with the actual plugin name.
      3. Writes the rendered text to the actual file inside the plugin directory.

    Args:
        template_path (Path): The path to the template file.
        target_path (Path): The path where the new file will be created.
        name (str): The short name of your plugin (e.g. 'awesome').
                    The final project folder would typically be 'efr-awesome'.
        description (str): A short description of the plugin.
    """

    # Check that input and output files exist
    if not template_path.exists():
        raise FileNotFoundError(f"Template file not found: {template_path}")

    if not target_path.exists():
        raise FileExistsError(f"File '{target_path}' already exists. Aborting to avoid overwriting.")

    # 2) Read the template content
    template_content = template_path.read_text(encoding="utf-8")

    # 3) Format the string with the plugin name
    rendered_content = template_content.format(name=name, description=description)


    # 4) Write the final content out
    target_path.write_text(rendered_content, encoding="utf-8")

    click.secho(f"\t{target_path.name} initialized for plugin '{name}' at: {target_path.resolve()}", fg="green")


def init_readme(plugin_dir: Path, name: str, description: str):
    """
    Initialize a README.md file for the new efr plugin project, from the template.

    Args:
        plugin_dir (Path): The path to the plugin directory where README.md will be created.
        name (str): The short name of your plugin (e.g. 'awesome').
                    The final project folder would typically be 'efr-awesome'.
        description (str): A short description of the plugin.
    """

    template_path = Path(__file__).parent / "templates" / "README.md.template"

    target_path = plugin_dir / "README.md"

    _init_file(template_path, target_path, name, description)


def init_setup_py(plugin_dir: Path, name: str, description: str):
    """
    Initialize a setup.py file for the new efr plugin project, from the template.

    Args:
        plugin_dir (Path): The path to the plugin directory where setup.py will be created.
        name (str): The short name of your plugin (e.g. 'awesome').
                    The final project folder would typically be 'efr-awesome'.
        description (str): A short description of the plugin.
    """

    template_path = Path(__file__).parent / "templates" / "setup.py.template"

    target_path = plugin_dir / "setup.py"

    _init_file(template_path, target_path, name, description)

def init_cli_py(plugin_dir: Path, name: str, description: str):
    """
    Initialize a cli.py file for the new efr plugin project, from the template.

    Args:
        plugin_dir (Path): The path to the plugin directory where cli.py will be created.
        name (str): The short name of your plugin (e.g. 'awesome').
                    The final project folder would typically be 'efr-awesome'.
        description (str): A short description of the plugin.
    """

    template_path = Path(__file__).parent / "templates" / "cli.py.template"

    target_path = plugin_dir / name / "cli.py"

    _init_file(template_path, target_path, name, description)


