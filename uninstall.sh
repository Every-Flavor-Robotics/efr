#!/usr/bin/env bash
set -e

EFR_HOME="$HOME/.efr"
GLOBAL_BIN="$HOME/.local/bin/efr"

# Remove the global command wrapper
if [ -f "$GLOBAL_BIN" ]; then
    echo "==> Removing global efr command..."
    rm "$GLOBAL_BIN"
else
    echo "==> Global efr command not found, skipping."
fi

# Remove the virtual environment and EFRC home directory
if [ -d "$EFR_HOME" ]; then
    echo "==> Removing efr virtual environment and related files..."
    rm -rf "$EFR_HOME"
else
    echo "==> efr directory not found, skipping."
fi

echo "==> efr successfully uninstalled!"
