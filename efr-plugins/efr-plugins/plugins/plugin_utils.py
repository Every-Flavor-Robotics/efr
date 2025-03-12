import ast
import os
import subprocess
from pathlib import Path

import click
import pkg_resources
import requests
import toml

REGISTRY_URL = (
    "https://raw.githubusercontent.com/Every-Flavor-Robotics/efr/"
    "refs/heads/main/efr-plugins/efr-plugins/plugins/plugin_registry.json"
)


def create_new_plugin_project(path: Path, name: str):
    """
    Create a skeleton directory structure for a new efr plugin project.

    This function generates:
      1. A main directory named efr-<name>.
      2. A Python package directory matching 'name'.
      3. Touch setup.py, __init__.py, cli.py, and install.sh in the package.
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
        raise FileExistsError(
            f"Directory '{plugin_dir}' already exists. Aborting to avoid overwriting."
        )

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

    # 7) Create install.sh
    install_file = plugin_dir / "install.sh"
    install_file.touch()

    return plugin_dir


def _init_file(template_path: str, target_path: Path, format_strings: dict):
    """
    Initialize a file from the templates folder for the new efr plugin project.

    This function:
      1. Reads the template file from the local 'templates' folder.
      2. Substitutes placeholders (e.g., '{name}' '{description}') with the actual plugin name.
      3. Writes the rendered text to the actual file inside the plugin directory.

    Args:
        template_path (Path): The path to the template file.
        target_path (Path): The path where the new file will be created.
        format_strings (Dict): A dictionary containing the format strings to be replaced in the template.
    """

    # Check that input and output files exist
    if not template_path.exists():
        raise FileNotFoundError(f"Template file not found: {template_path}")

    if not target_path.exists():
        raise FileExistsError(
            f"File '{target_path}' already exists. Aborting to avoid overwriting."
        )

    # 2) Read the template content
    template_content = template_path.read_text(encoding="utf-8")

    # 3) Format the string with the plugin name
    rendered_content = template_content.format(**format_strings)

    # 4) Write the final content out
    target_path.write_text(rendered_content, encoding="utf-8")

    name = format_strings.get("name", "unknown")

    click.secho(
        f"\t{target_path.name} initialized for plugin '{name}' at: {target_path.resolve()}",
        fg="green",
    )


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

    _init_file(template_path, target_path, {"name": name, "description": description})


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

    _init_file(template_path, target_path, {"name": name, "description": description})


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

    _init_file(template_path, target_path, {"name": name, "description": description})


def _get_git_details(plugin_dir: Path) -> dict:
    """
    Get the git details for the plugin directory.

    Args:
        plugin_dir (Path): The path to the plugin directory.

    Returns:
        dict: A dictionary containing the relative path of plugin_dir to the git repository root and the remote URL.

    Raises:
        FileNotFoundError: If the .git directory is not found.
    """

    # Check if the directory is inside a git repository
    try:
        repo_root = (
            subprocess.check_output(
                ["git", "-C", str(plugin_dir), "rev-parse", "--show-toplevel"],
                stderr=subprocess.STDOUT,
            )
            .strip()
            .decode("utf-8")
        )
    except subprocess.CalledProcessError:
        raise FileNotFoundError(f"No git repository found for directory: {plugin_dir}")

    # Get the relative path of plugin_dir to the git repository root
    relative_path = os.path.relpath(plugin_dir, repo_root)

    # Get the remote URL
    try:
        remote_url = (
            subprocess.check_output(
                ["git", "-C", str(plugin_dir), "config", "--get", "remote.origin.url"],
                stderr=subprocess.STDOUT,
            )
            .strip()
            .decode("utf-8")
        )
    except subprocess.CalledProcessError:
        remote_url = None

    # If remote URL is ssh, convert it to https
    if remote_url and remote_url.startswith("git@"):
        remote_url = remote_url.replace(":", "/").replace("git@", "https://")

    return {"relative_path": relative_path, "remote_url": remote_url}


def init_install_sh(plugin_dir: Path, name: str):
    """
    Initialize an install.sh file for the new efr plugin project, from the template.

    Args:
        plugin_dir (Path): The path to the plugin directory where install.sh will be created.
    """

    template_path = Path(__file__).parent / "templates" / "install.sh.template"

    target_path = plugin_dir / "install.sh"

    git_details = _get_git_details(plugin_dir)

    _init_file(
        template_path,
        target_path,
        {
            "plugin_repo": git_details["remote_url"],
            "plugin_dir": git_details["relative_path"],
            "name": name,
        },
    )


def get_github_raw_url(plugin_dir: Path, file_path: Path) -> str:
    """
    Get the raw GitHub URL for a file in the plugin directory.

    Args:
        plugin_dir (Path): The path to the plugin directory.
        file_path (Path): The path to the file in the plugin directory.

    Returns:
        str: The raw GitHub URL for the file.
    """

    git_details = _get_git_details(plugin_dir)

    if not git_details["remote_url"]:
        raise ValueError(f"Remote URL not found for plugin directory: {plugin_dir}")

    print(git_details["remote_url"])
    # Construct the raw URL
    raw_url = (
        git_details["remote_url"]
        .replace(".git", "")
        .replace("github.com", "raw.githubusercontent.com")
    )

    # Append the branch name
    raw_url += "/refs/heads/main"

    # Append the relative path of the file
    raw_url += f"/{git_details['relative_path']}/{file_path.name}"

    return raw_url


def _get_description_from_toml(toml_file: Path) -> str:
    data = toml.load(toml_file)
    # Description could be in different locations; check common ones.
    description = data.get("project", {}).get("description")
    if description is None:
        description = data.get("tool", {}).get("poetry", {}).get("description")
    if description is None:
        raise ValueError("Description not found in TOML file")
    return description


def _get_description_from_setup(setup_file: Path) -> str:
    with open(setup_file, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=str(setup_file))

    description = None
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and getattr(node.func, "id", None) == "setup":
            for keyword in node.keywords:
                if keyword.arg == "description":
                    # Only works if the description is a literal string.
                    if isinstance(keyword.value, ast.Str):
                        description = keyword.value.s
                    break
        if description:
            break
    if description is None:
        raise ValueError("Description not found in setup.py")
    return description


def get_description(plugin_dir: Path) -> str:
    setup_file = plugin_dir / "setup.py"
    toml_file = plugin_dir / "pyproject.toml"

    if toml_file.exists():
        return _get_description_from_toml(toml_file)
    elif setup_file.exists():
        return _get_description_from_setup(setup_file)
    else:
        raise FileNotFoundError(
            f"Neither pyproject.toml nor setup.py found in plugin directory: {plugin_dir}"
        )


def retrieve_registry():
    """
    Retrieve the plugin registry from the GitHub repository.
    """
    try:
        response = requests.get(REGISTRY_URL)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        click.secho(f"Error fetching registry: {e}", fg="red")
        return None


def is_plugin_installed(plugin_name: str) -> bool:
    """
    Checks if the plugin (assuming PyPI package named 'efr-{plugin_name}') is installed.
    """
    installed_packages = {
        dist.project_name.lower() for dist in pkg_resources.working_set
    }
    candidate_name = f"efr-{plugin_name}".lower()
    return candidate_name in installed_packages
