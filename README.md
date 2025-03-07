
<h1 align="center">🚀 | Every Flavor Robotics CLI Tool (efr) | 🚀</h1>

<p align="center">
  Your one-stop command line interface for all of the essential EFR goodies
</p>

---

## Table of Contents
- [Table of Contents](#table-of-contents)
- [Project Objectives](#project-objectives)
- [Installation](#installation)
  - [Install in editable mode:](#install-in-editable-mode)
- [Usage](#usage)
- [Creating Plugins](#creating-plugins)

---

## Project Objectives
Think of `efr` as a toolbelt for Every Flavor's various software tools: it is a central place to find all of the utilities we've built up to speed up our workflow and reduce our mistakes.

The project has three main objectives:


1. **Centralize Tools**: Offer a single CLI entry point for various teams, whether you're working on software dev, video editing, pcb design, or anything else.
2. **Extensible Architecture**: Support a robust plugin system, allowing each team to add new commands without touching the core codebase.
3. **Ease of Use**: Offer straightforward and self-explanatory commands, with detailed help messages for each subcommand. You shouldn't need to read any docs or talk to Swapnil to get started.

---

## Installation
Below is a quick, one-line terminal command to clone this repository and install **efr**:

MacOS/Linux:
```bash
curl -s https://raw.githubusercontent.com/Every-Flavor-Robotics/efr/main/install.sh | bash
```

Windows:
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://raw.githubusercontent.com/Every-Flavor-Robotics/efr/main/install.ps1 | iex"
```

The install script does the following:
1. **Clone** the repository from GitHub.
2. **Move** into the `efr` folder.
3. **Upgrade pip** to the latest version (best practice).
4. **Install** `efr` in editable mode, pulling in any required dependencies.
5. **If** anything fails, it prints an error message and **removes** the cloned folder to leave a clean environment.


### Install in editable mode:
If you're developing or contributing to **efr**, you can install it in editable mode. This way, you can make changes to the code and see them reflected immediately.

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

