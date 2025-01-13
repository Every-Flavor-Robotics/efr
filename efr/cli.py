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

        # Title line
        click.secho(
            "\n🚀 | Every Flavor Robotics Command Line Tool | 🚀  ",
            fg="cyan",
            bold=True,
        )

        # Version line
        click.secho(f"Version: {version}\n", fg="green", bold=True)

        # Description
        click.secho(
            "Plugins are the heart of efr: they provide the functionality for all of the various tasks.",
            fg="bright_magenta",
        )

        # Installed plugins
        click.secho("Installed plugins:", fg="bright_magenta", bold=True)
        plugin_list = list(pkg_resources.iter_entry_points("efr.plugins"))
        if plugin_list:
            for entry_point in plugin_list:
                click.echo(f"  • {entry_point.name}")
        else:
            click.secho("  (No plugins found)", fg="yellow")

        click.secho(
            "\nTo see what each plugin does, run 'efr <plugin_name>'",
            fg="bright_magenta",
        )

        click.secho(
            "To see a list of installable plugins, run 'efr plugins list'",
            fg="bright_magenta",
        )

        # Documentation link
        click.echo(
            "\nFor more documentation, check out:\n"
            "  https://github.com/Every-Flavor-Robotics/efr"
        )

        # Usage help
        click.secho("\nUsage:", bold=True)
        click.echo("  efr [COMMAND] [ARGS]...")

        # Extra help
        click.echo("Run 'efr --help' for more info.")
        ctx.exit(0)


# Auto-discover plugins: each plugin is a Click command or group
for entry_point in pkg_resources.iter_entry_points("efr.plugins"):
    plugin = entry_point.load()
    cli.add_command(plugin)
