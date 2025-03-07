# gh Plugin for efr CLI

Convenience tools for interacting with efr gh repos

--

## Table of Contents

- [gh Plugin for efr CLI](#gh-plugin-for-efr-cli)
  - [Table of Contents](#table-of-contents)
  - [Available Commands](#available-commands)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
    - [1. Install efr](#1-install-efr)
    - [2. Install the gh Plugin](#2-install-the-gh-plugin)

---

## Available Commands

- **init**: Initializes a GitHub repository with default EFR settings.
  - Creates a `README.md` file with a user-defined name, description, and emoji.
  - Downloads and adds an appropriate `LICENSE` file.
  - Generates a `.gitignore` file based on selected development tools.
  - Optionally commits these changes to the repository.

- **list**: Lists repositories within the Every-Flavor-Robotics GitHub organization.
  - Supports fuzzy search to filter repositories by name.
  - Displays repositories along with descriptions.

- **clone**: Clones a repository from the Every-Flavor-Robotics GitHub organization.
  - Supports both HTTPS and SSH cloning methods.

- **togprot**: Toggles the GitHub repository remote URL between HTTPS and SSH.
  - Useful for switching authentication methods when interacting with repositories.

---

## Prerequisites

Before using this plugin, ensure that you have the following:

1. **Python 3.7+**
2. **Click** (>= 7.0) - for CLI interactions
3. **Questionary** - for interactive prompts
4. **Requests** - for making API calls to GitHub
5. **efr** CLI installed and working on your system
6. A valid GitHub account with access to the Every-Flavor-Robotics organization
7. (Optional) GitHub Personal Access Token (PAT) to avoid API rate limits

---

## Installation

### 1. Install efr

If not already installed, follow the instructions [here](https://github.com/Every-Flavor-Robotics/efr?tab=readme-ov-file#installation).

### 2. Install the gh Plugin

Clone or download the efr-gh repository, then install it with pip:

```bash
git clone https://github.com/Every-Flavor-Robotics/efr.git
cd efr/efr-plugins/efr-gh
pip install .