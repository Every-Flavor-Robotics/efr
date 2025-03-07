# setup.py
from setuptools import find_packages, setup

setup(
    name="efr-plugins",
    version="0.1.0",
    author="Swapnil Pande",
    author_email="support@everyflavorrobotics.com",
    description="Utilites for managing plugins for `efr` CLI",
    include_package_data=True,
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
    package_data={
        "plugins": ["templates/*"],  # Ensure the templates directory is included
    },
)
