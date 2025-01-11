# MotorGo Plugin for efr

**efr-motorgo** is a plugin for the **efr** CLI tool, providing utilities for developing for the MotorGo ecosystem.

---

## Table of Contents

- [MotorGo Plugin for efr](#motorgo-plugin-for-efr)
  - [Table of Contents](#table-of-contents)
  - [Avaiable Commands](#avaiable-commands)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)

---

## Avaiable Commands

- **boards**: Utilities for handling custom MotorGo board definitions.
  - **install**: Installs a custom board definition and variant for PlatformIO.
  - **uninstall**: Removes a custom board definition and variant from PlatformIO.

---

## Prerequisites

1. **Python 3.7+**
2. **Click** (>= 7.0)
3. **Questionary** for interactive prompts
4. **efr** CLI installed and functioning in your environment.
5. A working [PlatformIO](https://platformio.org/) setup with the `arduino-esp32` framework and `espressif32` platforms installed.

---

## Installation

1. Install efr

If not already installed, follow instructions [here](https://github.com/Every-Flavor-Robotics/efr?tab=readme-ov-file#installation).

2. Install the MotorGo Plugin

Clone or download the efr-motorgo repository, then install it with pip:

```bash
git clone https://github.com/Every-Flavor-Robotics/efr.git
cd efr/efr-plugins/efr-motorgo
pip install .
```

This will register the MotorGo plugin with efr, making its commands available in the efr CLI.