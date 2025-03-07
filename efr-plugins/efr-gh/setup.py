# setup.py
from setuptools import find_packages, setup

setup(
    name="efr-gh",
    version="0.1.0",
    author="Swapnil Pande",
    author_email="swapnil@everyflavorrobotics.com",
    description="Convenience tools for interacting with efr gh repos.",
    packages=find_packages(),
    install_requires=[
        "Click>=7.0",  # Ensure Click is installed
        "questionary>=1.9.0",  # Ensure questionary is installed
    ],
    entry_points={
        # Register your subcommand under the efr.plugins group
        "efr.plugins": [
            "gh=gh.cli:gh",
        ],
    },
    python_requires=">=3.7",
    package_data={
        "gh": ["templates/*"],  # Ensure the templates directory is included
    },
)
