
<p align="center">
  <img src="https://user-images.githubusercontent.com/PLACEHOLDER/efr-logo.png" alt="efr Logo" width="200"/>
</p>

<h1 align="center">🚀 | Every Flavor Robotics CLI Tool (efr) | 🚀</h1>

<p align="center">
  Your one-stop command line interface for projects, plugins, and productivity.
</p>

---

## Table of Contents
- [Table of Contents](#table-of-contents)
- [Project Objectives](#project-objectives)
- [Installation](#installation)
- [Usage](#usage)
- [Creating Plugins](#creating-plugins)
- [Contributing](#contributing)

---

## Project Objectives
1. **Centralize Tools**: Offer a single CLI entry point for various teams—whether you’re working on video editing, board design, or something else.
2. **Extensible Architecture**: Support a robust plugin system, allowing each team to add new commands without touching the core codebase.
3. **Ease of Use**: Offer straightforward commands and a user-friendly help system.
4. **Scalability**: Ensure that as your organization grows and new tools are added, **efr** can seamlessly keep up.

---

## Installation
Below is a quick, one-line terminal command to clone this repository and install **efr** in [editable mode](https://pip.pypa.io/en/stable/cli/pip_install/#cmdoption-e). This will automatically clean up if it encounters errors, ensuring a smooth install process:

```bash
git clone https://github.com/Every-Flavor-Robotics/efr.git && cd efr && pip install --upgrade pip && pip install -e . || (echo "Install failed, cleaning up..." && cd .. && rm -rf efr)
```

Here’s what this does:
1. **Clone** the repository from GitHub.
2. **Move** into the `efr` folder.
3. **Upgrade pip** to the latest version (best practice).
4. **Install** `efr` in editable mode, pulling in any required dependencies.
5. **If** anything fails, it prints an error message and **removes** the cloned folder to leave a clean environment.

Alternatively, you can just manually clone and install:
```bash
git clone https://github.com/Every-Flavor-Robotics/efr.git
cd efr
pip install -e .
```

---

## Usage
Once installed, you can run:
```bash
efr
```
You’ll see:
- **Tool Information**: Version, a brief description, and usage instructions.
- **Installed Plugins**: A list of plugin commands that are immediately available.

To see detailed help on any subcommand, simply run:
```bash
efr <subcommand> --help
```

---

## Creating Plugins
One of **efr**’s main goals is modular extensibility. We’ve documented the process in the [plugin_docs.md](https://github.com/Every-Flavor-Robotics/efr/blob/main/plugin_docs.md). Highlights:

1. **Create** a new Python package with a Click command in a file (e.g., `cli.py`).
2. **Register** it under the `efr.plugins` entry point in your `setup.py` (or `pyproject.toml`).
3. **Install** your plugin package, and it appears automatically when you run `efr`.

For a quick start, check out our official [Creating a New **efr** Plugin](https://github.com/Every-Flavor-Robotics/efr/blob/main/plugin_docs.md) guide.

---

## Contributing
We love contributions—whether it’s adding new functionality, improving documentation, or fixing bugs! To get started:

1. Fork this repository and clone your fork.
2. Create a branch for your feature or fix.
3. Commit your changes, then open a pull request against **main**.

Once approved, we’ll merge it, and your changes become part of the **efr** platform.

---
