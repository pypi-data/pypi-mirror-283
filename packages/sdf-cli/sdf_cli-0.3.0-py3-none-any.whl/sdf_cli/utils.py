import subprocess
import os
import sys
from typing import Optional
from .version import SDF_CLI_VERSION
from .constants import SDF_BINARY
from .install import install_binary

def get_binary_path(package_dir: Optional[str] = None) -> str:
    """Return the path of the installed binary."""
    if package_dir is None:
        package_dir = os.path.dirname(__file__)
    binary_path = os.path.join(package_dir, 'binaries', SDF_BINARY)
    if not os.path.isfile(binary_path):
        try:
            binary_path = install_binary(package_dir)
        except Exception as e:
            raise FileNotFoundError(f"SDF CLI Failed to install: {e}")
    return binary_path

def run_binary(binary_path: Optional[str] = None, *args):
    """Run the installed binary."""
    if binary_path is None:
        binary_path = get_binary_path()
    os.execvp(binary_path, [binary_path] + [*args] + sys.argv[1:])

def get_binary_version():
    """Return the version of the installed binary."""
    return SDF_CLI_VERSION