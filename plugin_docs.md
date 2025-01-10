# Creating a New **efr** Plugin

This guide shows you how to build and register a new plugin for the **efr** command-line tool. By following these steps, you’ll end up with a standalone Python package that, when installed, automatically appears under `efr` as a new subcommand.

---

## 1. Overview

- **efr** is a CLI built with [Click](https://click.palletsprojects.com) and uses **entry points** for a plugin system.
- Each plugin is simply a Python package that defines:
  1. A Click command or group.
  2. An entry point under the `efr.plugins` group in its setup configuration (e.g., `setup.py` or `pyproject.toml`).

Once installed (`pip install ...`), your plugin’s subcommand(s) will appear when you run `efr --help` or `efr` without arguments.

---

## 2. Project Structure

Assume you want to create a plugin named **`efr-awesome`**. A simple layout might look like this:

```
efr-awesome/
├── awesome
│   ├── __init__.py
│   └── cli.py
└── setup.py (or pyproject.toml)
```

### `cli.py` Example

In `cli.py`, define a single Click command or a group of commands:

```python
# awesome/cli.py
import click

@click.command(name="awesome")
def awesome_cmd():
    """
    An 'awesome' subcommand for efr.
    """
    click.echo("Running something awesome!")
```

---

## 3. Defining the Entry Point

In your **`setup.py`**, declare how this package hooks into `efr.plugins`. For example:

```python
# setup.py
from setuptools import setup, find_packages

setup(
    name="efr-awesome",
    version="0.1.0",
    author="Your Name or Company",
    author_email="you@example.com",
    description="An awesome plugin for the efr CLI tool",
    packages=find_packages(),
    install_requires=[
        "Click>=7.0",  # Ensure Click is installed
    ],
    entry_points={
        # Register your subcommand under the efr.plugins group
        "efr.plugins": [
            "awesome=awesome.cli:awesome_cmd",
        ],
    },
    python_requires='>=3.7',
)
```

> **Note**: If you’re using **`pyproject.toml`** instead of **`setup.py`**, you’d define something similar under `[project.entry-points."efr.plugins"]`.

---

## 4. Installing and Testing

1. **Install the Plugin Locally** (in editable/development mode):
   ```bash
   cd /path/to/efr-awesome
   pip install -e .
   ```
2. **Check if It’s Registered**:
   ```bash
   efr
   ```
   You should see `awesome` listed among the available commands.

3. **Run the Awesome Command**:
   ```bash
   efr awesome
   ```
   It should display the output from your `awesome_cmd` function, for example:
   ```
   Running something awesome!
   ```

---

## 5. Versioning and Distribution

- **Version your plugin**: Update the `version` in `setup.py` or `pyproject.toml` to release new features or fixes.
- **Distribute**:
  - Publish to an internal PyPI (for company-internal distribution) or to PyPI.org if it’s open source.
  - Once installed in any environment that also has `efr` installed, your plugin is immediately available.

---

## 6. Summary

1. **Create a Click command** in a Python package.
2. **Register** it under the `efr.plugins` entry point.
3. **Install** the plugin so that `efr` can discover it.

That’s it—your new subcommand is now part of the **efr** ecosystem. Enjoy building and sharing tools across your teams!
```