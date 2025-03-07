"""cli.py

CLI entry point for the gh plugin.
Convenience tools for interacting with efr gh repos.
"""

import os
import subprocess
import textwrap
from difflib import get_close_matches
from pathlib import Path

import click
import questionary
import requests

repo_list = None


def _get_all_repos(org, token=None):
    """
    Retrieve all repositories for the given GitHub organization.

    Args:
        org (str): The GitHub organization name.
        token (str, optional): Personal access token for GitHub API. Helps avoid rate limits.

    Returns:
        list: A list of repository JSON objects.
    """
    global repo_list

    if not repo_list:
        repos = []
        url = f"https://api.github.com/orgs/{org}/repos"
        headers = {}
        if token:
            headers["Authorization"] = f"token {token}"

        while url:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an error for bad responses
            repos.extend(response.json())

            # GitHub API paginates results. Check for the 'Link' header to find the next page.
            if "link" in response.headers:
                links = requests.utils.parse_header_links(response.headers["link"])
                url = None  # Reset URL
                # Look for a link with rel="next"
                for link in links:
                    if link.get("rel") == "next":
                        url = link.get("url")
                        break
            else:
                url = None  # No pagination header found, so we're done

        repo_list = repos

    return repo_list


def complete_repos(ctx, args, incomplete):
    """
    Autocompletion function for repository names.

    This function retrieves all repositories for the specified organization and
    returns a list of repo names that start with the provided incomplete text.
    """
    repos = _get_all_repos("Every-Flavor-Robotics")
    print(repos)
    return [repo["name"] for repo in repos if repo["name"].startswith(incomplete)]


@click.group(name="gh")
@click.pass_context
def gh(ctx):
    """
    A group of commands for the gh plugin.
    """
    if ctx.invoked_subcommand is None:
        # Optionally, print help or decorative info here.
        pass


@gh.command()
def init():
    """
    Initialize a github repo with the default efr settings.
    """

    # Get the repo root directory
    try:
        repo_root = Path(
            subprocess.check_output(
                ["git", "-C", "./", "rev-parse", "--show-toplevel"],
                stderr=subprocess.STDOUT,
            )
            .strip()
            .decode("utf-8")
        )
    except subprocess.CalledProcessError:
        raise FileNotFoundError(
            "No git repository found. Please run this command in the git repository you want to set up."
        )

    click.secho(f"Initializing repository in {repo_root}\n", fg="green")

    click.secho("Step 1: Setting up the README", fg="cyan")

    # Check if the README.md file exists
    readme_path = repo_root / "README.md"
    skip_readme = False

    if readme_path.exists():
        if not click.confirm("README.md already exists. Do you want to overwrite it?"):
            click.secho("Skipping README setup.", fg="yellow")
            skip_readme = True
        else:
            click.secho("Overwriting README.md...", fg="green")
            readme_path.unlink()

    if not skip_readme:
        repo_name = click.prompt("Enter the repository name", default=repo_root.name)
        repo_description = click.prompt("Enter a description for the repository")
        emoji = click.prompt("Choose an emoji for the repository", default="🤖")

        template_path = Path(__file__).parent / "templates" / "README.md.template"
        template_content = template_path.read_text(encoding="utf-8")
        readme_content = template_content.format(
            name=repo_name, description=repo_description, emoji=emoji
        )
        readme_path.write_text(readme_content, encoding="utf-8")

        click.secho("README.md created successfully.", fg="green")

    click.secho("\nStep 2: Setting up the LICENSE", fg="cyan")
    HARDWARE_LICENSE_PATH = "https://raw.githubusercontent.com/Every-Flavor-Robotics/licenses/refs/heads/main/hardware_license.md"
    SOFTWARE_LICENSE_PATH = "https://raw.githubusercontent.com/Every-Flavor-Robotics/licenses/refs/heads/main/software_license.md"

    project_type = questionary.select(
        "Would you like to include the hardware or software license? Optionally, select 'none' to skip the license setup.",
        choices=["hardware", "software", "none"],
    ).ask()

    if project_type != "none":
        license_url = (
            HARDWARE_LICENSE_PATH
            if project_type == "hardware"
            else SOFTWARE_LICENSE_PATH
        )
        license_path = repo_root / "LICENSE"
        license_path.write_text(requests.get(license_url).text, encoding="utf-8")
        click.secho("LICENSE created successfully.", fg="green")

    click.secho("\nStep 3: Setting up the .gitignore", fg="cyan")
    gitignore_templates = {
        "Python": "https://www.toptal.com/developers/gitignore/api/python",
        "PlatformIO": "https://www.toptal.com/developers/gitignore/api/platformio",
        "Rust": "https://www.toptal.com/developers/gitignore/api/rust",
    }

    selected_templates = questionary.checkbox(
        "Which tools are you using for this project? (Select none to skip setting up .gitignore)",
        choices=list(gitignore_templates.keys()),
    ).ask()

    if selected_templates:
        gitignore_content = "".join(
            requests.get(gitignore_templates[t]).text for t in selected_templates
        )
        (repo_root / ".gitignore").write_text(gitignore_content, encoding="utf-8")
        click.secho(".gitignore created successfully.", fg="green")

    if click.confirm("Would you like to commit these changes?"):
        if not skip_readme:
            subprocess.run(["git", "add", "README.md"], cwd=repo_root)
        if project_type != "none":
            subprocess.run(["git", "add", "LICENSE"], cwd=repo_root)
        if selected_templates:
            subprocess.run(["git", "add", ".gitignore"], cwd=repo_root)

        subprocess.run(
            ["git", "commit", "-m", "Setup repository with efr defaults"], cwd=repo_root
        )
        click.secho("Changes committed successfully.", fg="green")

    click.secho("\nSetup complete!", fg="green")


@gh.command(name="list")
@click.argument("pattern", required=False)
def list_repos(pattern):
    """
    List repositories in the organization that match the provided fuzzy search pattern.

    If no pattern is provided, all repository names will be listed.
    """
    repos = _get_all_repos("Every-Flavor-Robotics")

    # Build a dictionary of repo_name -> repo_description
    repo_descriptions = {repo["name"]: repo["description"] for repo in repos}
    repo_names = list(repo_descriptions.keys())

    # Filter repositories based on the fuzzy search pattern if provided
    if pattern:
        matches = get_close_matches(pattern, repo_names, n=len(repo_names), cutoff=0.3)
        if not matches:
            click.secho("No matches found.", fg="red")
            return
        filtered_names = matches
        click.secho("Matching repositories:", fg="green", bold=True)
    else:
        filtered_names = repo_names
        click.secho("All repositories:", fg="green", bold=True)
        click.secho("To filter the list, provide a search pattern.", fg="yellow")
        click.secho("\tExample: efr gh list <pattern>", fg="yellow")

    if not filtered_names:
        click.secho("No repositories found.", fg="red")
        return

    # Determine column widths and create a divider line
    max_name_length = max(len(name) for name in filtered_names)
    desc_width = 70  # maximum width for description
    divider_length = max_name_length + 4 + desc_width  # spacing + description width
    divider = "-" * divider_length

    # Print header row
    header = f"{'Repository'.ljust(max_name_length)}    Description"
    click.secho(header, bold=True, fg="cyan")
    click.secho(divider, fg="cyan")

    # Print each repository in a table-like format with divider between rows.
    for name in sorted(filtered_names):
        desc = repo_descriptions.get(name) or ""
        # Wrap the description text to the desired width.
        wrapped_desc = textwrap.fill(desc, width=desc_width)
        # Split wrapped text into lines.
        lines = wrapped_desc.splitlines() if wrapped_desc else [""]
        # Print the repo name with the first line of its description.
        click.secho(f"{name.ljust(max_name_length)}    ", nl=False, fg="blue")
        click.secho(lines[0], fg="magenta")
        # Print any additional lines of the description indented.
        for continued_line in lines[1:]:
            click.secho(" " * (max_name_length + 4) + continued_line, fg="magenta")
        # Print a divider line after each repository row.
        click.secho(divider, fg="yellow")


@gh.command()
@click.argument("repo")
# Option to use ssh to clone, default is https
@click.option("--ssh", is_flag=True, help="Use SSH protocol to clone the repository.")
def clone(repo, ssh):
    """
    Clone a repository from the organization.

    The repo argument supports tab-completion based on the organization's repository names.
    """

    path = f"Every-Flavor-Robotics/{repo}"

    # Green, notify user that the repo is being cloned
    click.secho(f"Cloning repository '{path}'...", fg="green")

    # Determine the clone URL based on the protocol option
    if ssh:
        clone_url = f"git@github.com:{path}.git"
    else:
        clone_url = f"https://github.com/{path}.git"

    # Clone the repository using the git command
    result = subprocess.run(["git", "clone", clone_url], capture_output=True, text=True)

    if result.returncode == 0:
        click.secho(f"Repository '{path}' cloned successfully.", fg="green")
    else:
        click.secho(f"Failed to clone repository '{path}'.\n", fg="red")

        # Split the error message into lines, indent each line, then join them back
        indented_err = "\n".join("    " + line for line in result.stderr.splitlines())
        click.secho(indented_err, fg="red")


# Add a command that will quickly convert back and forth between ssh and https


@gh.command(
    name="togprot", help="Toggle the current repo between https and ssh protocols."
)
def toggle_protocol():
    """
    Toggle the current repository between HTTPS and SSH protocols.

    This command assumes the current working directory is a Git repository.
    """
    # Get the current remote URL for the 'origin' remote
    result = subprocess.run(
        ["git", "remote", "get-url", "origin"], capture_output=True, text=True
    )

    if result.returncode != 0:
        click.secho(
            "Failed to get the remote URL. Make sure you are in a github repo.",
            fg="red",
        )
        return

    https_prefix = "https://github.com/"
    ssh_prefix = "git@github.com:"

    current_url = result.stdout.strip()
    if current_url.startswith(https_prefix):
        new_url = current_url.replace(https_prefix, ssh_prefix)
        new_protocol = "ssh"
    elif current_url.startswith(ssh_prefix):
        new_url = current_url.replace(ssh_prefix, https_prefix)
        new_protocol = "https"
    else:
        click.secho("Unsupported URL format.", fg="red")
        return

    # Update the remote URL with the new protocol
    result = subprocess.run(
        ["git", "remote", "set-url", "origin", new_url], capture_output=True, text=True
    )

    if result.returncode == 0:
        click.secho(f"Protocol updated successfully to {new_protocol}.", fg="green")
    else:
        click.secho("Failed to update the protocol.", fg="red")


if __name__ == "__main__":
    gh()
