import subprocess
from setuptools import setup, find_packages

setup(
    name="acktool",
    version="0.1",
    py_modules=["acktool"], 
    packages=find_packages(),
    install_requires=[
        'validators',
        'django'
    ],
    entry_points={
        "console_scripts": [
            "acktool=CLI.cli_interface:main",
        ],
    },
)
