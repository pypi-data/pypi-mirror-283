from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("seatable_client")
except PackageNotFoundError:
    # package is not installed
    pass