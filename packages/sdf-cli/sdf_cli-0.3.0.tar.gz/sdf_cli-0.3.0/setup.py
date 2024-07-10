from setuptools import setup, find_packages
from pathlib import Path

version = {}
with open(Path(__file__).parent / "sdf_cli/version.py", encoding="utf8") as fp:
    exec(fp.read(), version)

SDF_CLI_VERSION = version['SDF_CLI_VERSION']

setup(
    name='sdf-cli',
    version=SDF_CLI_VERSION,
    packages=find_packages(),
    package_data={
        'sdf_cli': ['binaries/*'],
    },
    entry_points={
        'console_scripts': [
            'sdf = sdf_cli.utils:run_binary'
        ]
    },
    classifiers = [
        'Programming Language :: Python :: 3',
    ],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    # Add other metadata as required
)