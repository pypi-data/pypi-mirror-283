import platform
import urllib.request
import shutil
import stat
import os
from sdf_cli.version import SDF_CLI_VERSION
from sdf_cli.constants import SDF_BINARY

def install_binary(target_dir: str) -> str:
    system = platform.system().lower()
    arch = platform.machine().lower()

    if system == 'darwin':
        if arch == 'arm64':
            target = 'aarch64-apple-darwin'
        elif arch == 'x86_64':
            target = 'x86_64-apple-darwin'
    elif system == 'linux':
        if arch == 'x86_64':
            target = 'x86_64-unknown-linux-musl'
        elif arch == 'aarch64':
            target = 'aarch64-unknown-linux-gnu'
    else:
        raise RuntimeError(f'Unsupported platform: {system} {arch}')
    sdf_target = f'sdf-v{SDF_CLI_VERSION}-{target}'
    sdf_target_archive = f'{sdf_target}.tar.gz'
    # Download the binary to memory, untar it, and place contents to the target path
    url = f'https://cdn.sdf.com/releases/download/{sdf_target_archive}'
    # Ensure the target directory exists
    os.makedirs(target_dir, exist_ok=True)
    target_path = os.path.join(target_dir, SDF_BINARY)
    tmp_sdf_archive = os.path.join(target_dir, sdf_target_archive)
    with urllib.request.urlopen(url) as response:
        with open(tmp_sdf_archive, 'wb') as f:
            shutil.copyfileobj(response, f)
    shutil.unpack_archive(tmp_sdf_archive, target_dir)
    os.remove(tmp_sdf_archive)
    shutil.move(os.path.join(target_dir, sdf_target, SDF_BINARY), target_path)

    # Make the binary executable
    st = os.stat(target_path)
    os.chmod(target_path, st.st_mode | stat.S_IEXEC)
    return target_path