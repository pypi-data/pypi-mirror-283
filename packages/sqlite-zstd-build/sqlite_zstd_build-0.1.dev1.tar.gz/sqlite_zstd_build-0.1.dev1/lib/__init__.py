import sqlite3
from importlib.resources import files, as_file
from setuptools_scm import get_version

real_version = get_version(root="..")
pretend_version = get_version(root="..", local_scheme="no-local-version")
if pretend_version != real_version:
    __version__ = pretend_version
else:
    __version__ = real_version


def load(conn: sqlite3.Connection) -> None:
    lib = next(x for x in files(__name__).iterdir() if x.name.startswith("lib"))
    with as_file(lib) as ext:
        conn.load_extension(str(ext))
