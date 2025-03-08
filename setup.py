from setuptools import find_packages, setup

setup(
    name="efr",
    version="0.2.0",
    author="Swapnil Pande",
    author_email="support@everyflavorrobotics.com",
    description="A central CLI (efr) for common Every Flavor Robotics tools, using plugins via entry points",
    packages=find_packages(),
    install_requires=[
        "Click>=7.0",
        "questionary>=1.9.0",
        "setuptools>=75.8.2",
        "requests>=2.32.3",
    ],
    entry_points={
        "console_scripts": [
            # This defines the main 'efr' command (from efr/cli.py)
            "efr=efr.cli:cli",
        ],
        # Register built-in plugins so they’re automatically discovered
        "efr.plugins": [
            # Add more as needed
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
