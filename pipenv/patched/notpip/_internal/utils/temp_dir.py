from __future__ import absolute_import

import logging
import os.path
import tempfile

from pipenv.patched.notpip._internal.utils.misc import rmtree
from pipenv.vendor.vistir.compat import TemporaryDirectory

logger = logging.getLogger(__name__)


class TempDirectory(TemporaryDirectory):
    """Helper class that owns and cleans up a temporary directory.

    This class can be used as a context manager or as an OO representation of a
    temporary directory.

    Attributes:
        path
            Location to the created temporary directory or None
        delete
            Whether the directory should be deleted when exiting
            (when used as a contextmanager)

    Methods:
        create()
            Creates a temporary directory and stores its path in the path
            attribute.
        cleanup()
            Deletes the temporary directory and sets path attribute to None

    When used as a context manager, a temporary directory is created on
    entering the context and, if the delete attribute is True, on exiting the
    context the created directory is deleted.
    """

    def __init__(self, path=None, delete=None, kind="temp"):
        if not path:
            super(TempDirectory, self).__init__(prefix="pip-{0}".format(kind))
        else:
            self.name = path

        if path is None and delete is None:
            # If we were not given an explicit directory, and we were not given
            # an explicit delete option, then we'll default to deleting.
            delete = True

        self.path = os.path.realpath(self.name)
        self.delete = delete
        self.kind = kind
        if not self.delete:
            self._finalizer = None

    def cleanup(self):
        if self.delete:
            super(TempDirectory, self).cleanup()
        else:
            pass

    def __repr__(self):
        return "<{} {!r}>".format(self.__class__.__name__, self.path)

    def __enter__(self):
        return self

    def __exit__(self, exc, value, tb):
        if self.delete:
            self.cleanup()

    def create(self):
        """Create a temporary directory and store it's path in self.path
        """
        if self.path is not None:
            logger.debug(
                "Skipped creation of temporary directory: {}".format(self.path)
            )
            return
        # We realpath here because some systems have their default tmpdir
        # symlinked to another directory.  This tends to confuse build
        # scripts, so we canonicalize the path by traversing potential
        # symlinks here.
        self.path = os.path.realpath(
            tempfile.mkdtemp(prefix="pip-{}-".format(self.kind))
        )
        logger.debug("Created temporary directory: {}".format(self.path))
