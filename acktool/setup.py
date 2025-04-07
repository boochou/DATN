import subprocess
from setuptools import setup, find_packages

# Run setup.sh before installation
print("Executing setup.sh...")
subprocess.run(["bash", "setup.sh"], check=True)

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
            "acktool=acktool:main",
        ],
    },
)
