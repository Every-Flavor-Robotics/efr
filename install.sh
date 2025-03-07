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
    source $HOME/.local/bin/env
else
    echo "==> uv is already installed."
fi


# Check if virtual environment already exists
if [ -d "$VENV_DIR" ]; then
    echo "==> Virtual environment already exists. Skipping creation."
else
    echo "==> Setting up virtual environment with uv..."
    uv venv "$VENV_DIR"
fi

# Activate virtual environment
source "$VENV_DIR/bin/activate"

# Upgrade pip within the virtual environment
uv pip install --upgrade pip

# Clone efr repository if not already cloned
if [ -d "$EFR_HOME/efr-tmp" ]; then
    echo "==> Repository already cloned. Pulling latest changes..."
    cd "$EFR_HOME/efr-tmp" && git pull
else
    echo "==> Cloning efr repository..."
    git clone https://github.com/Every-Flavor-Robotics/efr.git "$EFR_HOME/efr-tmp"
    cd "$EFR_HOME/efr-tmp"
fi

# Install efr
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
GLOBAL_COMMAND="$HOME/.local/bin/efr"
if [ -f "$GLOBAL_COMMAND" ]; then
    echo "==> Global efr command already exists. Skipping creation."
else
    echo "==> Registering global efr command..."
    printf '#!/usr/bin/env bash\nsource "%s/bin/activate"\nefr "$@"\n' "$VENV_DIR" > "$GLOBAL_COMMAND"
    chmod +x "$GLOBAL_COMMAND"
fi

# Cleanup
echo "==> Cleaning up temporary files..."
cd "$HOME"
rm -rf "$EFR_HOME/efr-tmp"

# rm -- "$0"

echo "==> efr installation complete!"
echo "==> Run 'efr --help' to get started."
