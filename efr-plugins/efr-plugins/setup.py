# setup.py
from setuptools import setup, find_packages

setup(
    name="efr-plugins",
    version="0.1.0",
    author="Swapnil Pande",
    author_email="support@everyflavorrobotics.com",
    description="Utilites for managing plugins for `efr` CLI",
    packages=find_packages(),
    install_requires=[
        "Click>=7.0",  # Ensure Click is installed
        "questionary>=1.9.0",  # Ensure questionary is installed
    ],
    entry_points={
        # Register your subcommand under the efr.plugins group
        "efr.plugins": [
            "plugins=plugins.cli:plugins",
        ],
    },
    python_requires=">=3.7",
)
