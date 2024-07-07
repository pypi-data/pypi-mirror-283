from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("google_scraper")
except PackageNotFoundError:
    # package is not installed
    pass
