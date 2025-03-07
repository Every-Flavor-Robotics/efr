#!/usr/bin/env bash
set -e

EFRC_HOME="$HOME/.efr"
VENV_DIR="$EFRC_HOME/venv"

# Ensure required directories exist
mkdir -p "$EFRC_HOME"

# Clone efr repository into temporary directory
echo "==> Cloning efr repository..."
git clone https://github.com/Every-Flavor-Robotics/efr.git "$EFRC_HOME/efr-tmp"

# Set up the virtual environment with uv
echo "==> Setting up virtual environment with uv..."
uv venv "$VENV_DIR"

# Activate virtual environment
source "$VENV_DIR/bin/activate"

# Upgrade pip within the virtual environment
uv pip install --upgrade pip

# Install efr
cd "$EFRC_HOME/efr-tmp"
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
echo "#!/usr/bin/env bash\nsource \"$VENV_DIR/bin/activate\"\nefr \"\$@\"" > "$HOME/.local/bin/efr"
chmod +x "$HOME/.local/bin/efr"


# Cleanup
echo "==> Cleaning up temporary files..."
cd "$HOME"
rm -rf "$EFRC_HOME/efr-tmp"
rm -- "$0"

# Provide instructions to add to PATH
if ! grep -q "$VENV_DIR/bin" <<<"$PATH"; then
    echo -e "\nIMPORTANT: To run efr from anywhere, add the following line to your shell profile (e.g., ~/.bashrc or ~/.zshrc):"
    echo "export PATH=\"$VENV_DIR/bin:\$PATH\""
fi

echo "==> efr installation complete!"
