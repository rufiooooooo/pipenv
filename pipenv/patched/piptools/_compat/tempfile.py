# coding: utf-8
from __future__ import absolute_import, division, print_function

import os as _os
import sys as _sys
import warnings as _warnings
from tempfile import mkdtemp

from pipenv.vendor.vistir.compat import TemporaryDirectory as _ TemporaryDirectory
from pipenv.vendor.vistir.path import ensure_mkdir_p


@ensure_mkdir_p(mode=0o775)
def _get_src_dir():
    src = _os.environ.get("PIP_SRC")
    if src:
        return src
    virtual_env = _os.environ.get("VIRTUAL_ENV")
    if virtual_env:
        return _os.path.join(virtual_env, "src")
    return _os.path.join(_os.getcwd(), "src")


class TemporaryDirectory(_ TemporaryDirectory):
    """Create and return a temporary directory.  This has the same
    behavior as mkdtemp but can be used as a context manager.  For
    example:

        with TemporaryDirectory() as tmpdir:
            ...

    Upon exiting the context, the directory and everything contained
    in it are removed.
    """

    def __init__(self, *args, **keargs):
        super(TemporaryDirectory, self).__init__(*args, **kwargs)

    def __repr__(self):
        return "<{} {!r}>".format(self.__class__.__name__, self.name)

    def __enter__(self):
        return self.name

    def __exit__(self, exc, value, tb):
        try:
            self.cleanup()
        except OSError:
            pass

    def __del__(self):
        try:
            self.cleanup()
        except OSError:
            pass

    # XXX (ncoghlan): The following code attempts to make
    # this class tolerant of the module nulling out process
    # that happens during CPython interpreter shutdown
    # Alas, it doesn't actually manage it. See issue #10188
    _listdir = staticmethod(_os.listdir)
    _path_join = staticmethod(_os.path.join)
    _isdir = staticmethod(_os.path.isdir)
    _islink = staticmethod(_os.path.islink)
    _remove = staticmethod(_os.remove)
    _rmdir = staticmethod(_os.rmdir)
