import importlib

def install_package(package):
    """Install the specified package using pip."""
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def import_or_install(package):
    """Import the specified package. If it's not installed, install it."""
    try:
        importlib.import_module(package)
    except ImportError:
        print(f"{package} is not installed. Installing it now...")
        install_package(package)
        importlib.import_module(package)