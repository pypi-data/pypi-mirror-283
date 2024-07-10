# ------------------------------------------------------ Imports ----------------------------------------------------- #
import subprocess
import os
import stat
import platform
import sys
import time


def read_readme():
    with open(os.path.join(os.path.join(os.path.dirname(__file__), os.pardir), 'README.md'), 'r', encoding='utf-8') as f:
        return f.read()


def set_start_time() -> float:
    start_time = time.time()
    return start_time


def get_processing_time(start_time: float, unit='s') -> str:
    end_time = time.time()
    time_elapsed = end_time - start_time

    if unit == 's':
        return f'{round(time_elapsed, 2)} seconds'
    if unit == "m":
        return f'{round(time_elapsed/60, 2)} minutes'
    if unit == "h":
        return f'{round(time_elapsed/(60*60), 2)} hours'


def set_permissions(file_path, system_type):
    """
    Sets permissions for a file based on the system type.

    :param file_path: The path to the file.
    :type file_path: str
    :param system_type: The type of the system.
    :type system_type: str
    :raises ValueError: If the system type is not supported.
    """
    if system_type == "windows":
        subprocess.check_call(["icacls", file_path, "/grant", "*S-1-1-0:(F)"])
    elif system_type in ["linux", "mac"]:
        os.chmod(file_path, stat.S_IRWXU | stat.S_IRGRP | stat.S_IROTH)  # equivalent to 'chmod u+x'
    else:
        raise ValueError("Unsupported OS")


def get_virtual_env_root():
    """
    Gets the root directory of the virtual environment.

    :return: The root directory of the virtual environment.
    :rtype: str
    """
    python_exe = sys.executable
    virtual_env_root = os.path.dirname(os.path.dirname(python_exe))
    return virtual_env_root


def get_operating_system() -> str:
    """
    Gets the system and architecture information.

    :return: A tuple containing the system and architecture information.
    :rtype: tuple
    :raises ValueError: If the system or architecture is not supported.
    """
    system = platform.system().lower()
    if system == "darwin":
        system = "mac"
    elif system == "windows":
        system = "windows"
    elif system == "linux":
        system = "linux"
    else:
        raise ValueError("Unsupported OS type")

    return system


def get_architecture() -> str:
    detected_architecture = platform.machine().lower()
    if detected_architecture in ["x86_64", "amd64"]:
        system_architecture = "x86_64"
    elif "arm" in detected_architecture:
        system_architecture = "arm64"
    else:
        raise ValueError("Unsupported architecture")

    return system_architecture


# ----------------------------------------------------- Constants ---------------------------------------------------- #
BINARY_PATH = os.path.join(get_virtual_env_root(), 'bin')
GREEDY_COMPILED = "/home/horyzen/Projects/builds/Greedy/bin/greedy"

# Set the paths to the binaries based on the operating system
operating_system = get_operating_system()
architecture = get_architecture()
if operating_system == 'windows':
    GREEDY_PATH = os.path.join(BINARY_PATH, f'beast-binaries-{operating_system}-{architecture}', 'greedy.exe')
    DCM2NIIX_PATH = os.path.join(BINARY_PATH, f'beast-binaries-{operating_system}-{architecture}', 'dcm2niix.exe')
elif operating_system in ['linux', 'mac']:
    GREEDY_PATH = os.path.join(BINARY_PATH, f'beast-binaries-{operating_system}-{architecture}', 'greedy')
    DCM2NIIX_PATH = os.path.join(BINARY_PATH, f'beast-binaries-{operating_system}-{architecture}', 'dcm2niix')
else:
    raise ValueError('Unsupported OS')
