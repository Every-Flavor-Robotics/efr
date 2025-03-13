$EFR_HOME = "$env:USERPROFILE\.efr"
$VENV_DIR = "$EFR_HOME\venv"

# Ensure required directories exist
New-Item -ItemType Directory -Path $EFR_HOME -Force | Out-Null

# Check if uv is installed, install if necessary
if (-not (Get-Command "uv" -ErrorAction SilentlyContinue)) {
    Write-Host "==> uv not found. Installing uv..."
    Invoke-WebRequest "https://astral.sh/uv/install.ps1" -UseBasicParsing | Invoke-Expression

    # Explicitly update PATH for immediate use
    $env:PATH += ";$env:USERPROFILE\.cargo\bin;$env:USERPROFILE\.local\bin"
} else {
    Write-Host "==> uv is already installed."
}

# Check if virtual environment exists
if (Test-Path "$VENV_DIR") {
    Write-Host "==> Virtual environment already exists. Skipping creation."
} else {
    Write-Host "==> Setting up virtual environment with uv..."
    uv venv "$VENV_DIR" --python 3.12
}

# Activate virtual environment
& "$VENV_DIR\Scripts\Activate.ps1"

# Upgrade pip within the virtual environment
uv pip install --upgrade pip

# Clone efr repository or update if already cloned
if (Test-Path "$EFR_HOME\efr-tmp") {
    Write-Host "==> Repository already exists. Pulling latest changes..."
    Set-Location "$EFR_HOME\efr-tmp"
    git pull
} else {
    Write-Host "==> Cloning efr repository..."
    git clone https://github.com/Every-Flavor-Robotics/efr.git "$EFR_HOME\efr-tmp"
    Set-Location "$EFR_HOME\efr-tmp"
}

# Install efr
Write-Host "==> Installing efr package..."
uv pip install .

# Install efr plugins
if (Test-Path "efr-plugins\efr-plugins") {
    Set-Location "efr-plugins\efr-plugins"
    Write-Host "==> Installing efr plugins..."
    uv pip install .
} else {
    Write-Host "==> efr plugins directory not found, skipping plugin installation."
}

# Create global command wrapper
$GLOBAL_COMMAND = "$EFR_HOME\efr.ps1"
if (Test-Path "$GLOBAL_COMMAND") {
    Write-Host "==> Global efr command already exists. Skipping creation."
} else {
    Write-Host "==> Registering global efr command..."
    $scriptContent = @"
& `"$VENV_DIR\Scripts\Activate.ps1`"
efr `@args
deactivate
"@
    $scriptContent | Set-Content -Path $GLOBAL_COMMAND -Encoding UTF8
}

# Add command to user's PATH if not already added
$currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
if (-not $currentPath.Contains($EFR_HOME)) {
    Write-Host "==> Adding efr command to user PATH..."
    [Environment]::SetEnvironmentVariable("Path", "$currentPath;$EFR_HOME", "User")
} else {
    Write-Host "==> efr already in PATH. Skipping."
}

# Cleanup
Write-Host "==> Cleaning up temporary files..."
Set-Location $HOME
Remove-Item -Recurse -Force "$EFR_HOME\efr-tmp"

Write-Host "==> efr installation complete!"
Write-Host "==> Please restart your terminal or run `efr --help` in a new PowerShell session to get started."
