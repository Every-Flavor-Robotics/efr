#!/usr/bin/env bash
set -e

EFR_HOME="$HOME/.efr"
VENV_DIR="$EFR_HOME/venv"

# Ensure required directories exist
mkdir -p "$EFR_HOME"

# Check if uv is installed, install if necessary
if ! command -v uv &>/dev/null; then
    echo "==> uv not found. Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
else
    echo "==> uv is already installed."
fi

# Clone efr repository into temporary directory
echo "==> Cloning efr repository..."
git clone https://github.com/Every-Flavor-Robotics/efr.git "$EFR_HOME/efr-tmp"

# Set up the virtual environment with uv
echo "==> Setting up virtual environment with uv..."
uv venv "$VENV_DIR"

# Activate virtual environment
source "$VENV_DIR/bin/activate"

# Upgrade pip within the virtual environment
uv pip install --upgrade pip

# Install efr
cd "$EFR_HOME/efr-tmp"
echo "==> Installing efr package..."
uv pip install .

# Install efr plugins
if [ -d "efr-plugins/efr-plugins" ]; then
    cd efr-plugins/efr-plugins
    echo "==> Installing efr plugins..."
    uv pip install .
else
    echo "==> efr plugins directory not found, skipping plugin installation."
fi

# Create global command wrapper
echo "==> Registering global efr command..."
printf '#!/usr/bin/env bash\nsource "%s/bin/activate"\nefr "$@"\n' "$VENV_DIR" > "$HOME/.local/bin/efr"
chmod +x "$HOME/.local/bin/efr"


# Cleanup
echo "==> Cleaning up temporary files..."
cd "$HOME"
rm -rf "$EFR_HOME/efr-tmp"
# rm -- "$0"

echo "==> efr installation complete!"
echo "==> Run 'efr --help' to get started."
