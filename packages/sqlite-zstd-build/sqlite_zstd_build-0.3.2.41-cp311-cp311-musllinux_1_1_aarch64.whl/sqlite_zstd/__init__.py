import sqlite3
from importlib.resources import files, as_file

try:
    from setuptools_scm import get_version
    import pathlib

    root = pathlib.Path(__file__).parent.parent.parent.resolve()
    real_version = get_version(root=root, version_scheme="post-release")
    pretend_version = get_version(
        root=root, version_scheme="post-release", local_scheme="no-local-version"
    )
    if pretend_version != real_version:
        __version__ = pretend_version.replace("post", "")
    else:
        __version__ = real_version
    print(f"sqlite-zstd version: {__version__}")
except Exception as e:
    print(f"Failed to get sqlite-zstd version: {e}")
    __version__ = "0.0.0"


def load(conn: sqlite3.Connection) -> None:
    lib = next(x for x in files(__name__).iterdir() if x.name.startswith("lib"))
    with as_file(lib) as ext:
        conn.load_extension(str(ext))


print(__version__)
