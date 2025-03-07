"""cli.py

CLI entry point for the gh plugin.
Convenience tools for interacting with efr gh repos.
"""

import os
import subprocess
import textwrap
from difflib import get_close_matches

import click
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
@click.argument("repo", shell_complete=complete_repos)
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


if __name__ == "__main__":
    gh()
