# setup.py
from setuptools import setup, find_packages

setup(
    name="efr-motorgo",
    version="0.1.0",
    author="Swapnil Pande",
    author_email="support@everyflavorrobotics.com",
    description="Common utilities for MotorGo development",
    packages=find_packages(),
    install_requires=[
        "Click>=7.0",  # Ensure Click is installed
        "questionary>=1.9.0",  # Ensure questionary is installed
    ],
    entry_points={
        # Register your subcommand under the efr.plugins group
        "efr.plugins": [
            "motorgo=motorgo.cli:motorgo",
        ],
    },
    python_requires=">=3.7",
)
