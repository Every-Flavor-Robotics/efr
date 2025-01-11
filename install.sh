#!/usr/bin/env bash
set -e

echo "==> Installing efr..."

# 1) Clone the repository
git clone https://github.com/Every-Flavor-Robotics/efr.git

# 2) Enter the cloned directory
cd efr

# 3) Upgrade pip if desired, then install efr (non-editable mode)
pip install --upgrade pip
pip install .

echo "==> efr successfully installed!"

# 3) Install the plugins plugin (non-editable mode)
cd efr-plugins/efr-plugins
pip install .

# 4) Leave the repo directory and clean it up
cd ..
rm -rf efr

# 5) Remove this installer script
rm -- "$0"

echo "==> Cleanup complete."