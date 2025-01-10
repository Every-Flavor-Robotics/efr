# efr/cli.py
import click
import pkg_resources


def get_version():
    """
    Attempt to load efr's version from the installed package metadata.
    Fallback to "unknown" if not found.
    """
    try:
        dist = pkg_resources.get_distribution("efr")
        return dist.version
    except pkg_resources.DistributionNotFound:
        return "unknown"


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """
    efr - A central CLI for bundling modules from different projects.
    """
    if not ctx.invoked_subcommand:
        version = get_version()
        click.echo("Every Flavor Robotics command line tool")
        click.secho(f"Version: {version}", fg="green")

        click.echo("Installed plugins:")
        for entry_point in pkg_resources.iter_entry_points("efr.plugins"):
            click.echo(f"  - {entry_point.name}")

        click.echo("For details on creating and installing plugins, see: ")
        click.echo("\nUsage: efr [COMMAND] [ARGS]...")
        click.echo("Run 'efr --help' for more info.")
        ctx.exit(0)


# Auto-discover plugins: each plugin is a Click command or group
for entry_point in pkg_resources.iter_entry_points("efr.plugins"):
    plugin = entry_point.load()
    cli.add_command(plugin)
    cli.add_command(plugin)
