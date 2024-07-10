import sys
import shutil
import tempfile
from pathlib import Path
from typing import Generator
from contextlib import contextmanager

if sys.version_info < (3, 9):
    import importlib_resources
else:
    import importlib.resources as importlib_resources


@contextmanager
def resource_path(*args) -> Generator[Path, None, None]:
    """The resource is specified relative to `blissoda.resources`.

    .. code-block:: python

        with resource_path("exafs", "exafs.ows") a path:
            ...
    """
    source = importlib_resources.files(__name__).joinpath(*args)
    with importlib_resources.as_file(source) as path:
        yield path


def resource_filename(*args) -> str:
    """The resource is specified relative to `blissoda.resources`.

    .. code-block:: python

        filename = resource_filename("exafs", "exafs.ows")
    """
    with resource_path(*args) as path:
        if not path.exists():
            return str(path)  # resource does not exist
    if not path.exists():
        with resource_path(*args) as path:
            # resource was extract from zip: copy for persistency
            path_copy = Path(tempfile.mkdtemp()) / path.name
            shutil.copyfile(str(path), str(path_copy))
            path = path_copy
    return str(path)
