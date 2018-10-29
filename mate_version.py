import re
import subprocess
import sys
from collections import namedtuple

MateVersion = namedtuple("MateVersion", ["major", "minor", "patch"])
pattern = re.compile(
    b"(?P<major>\d+)\."
    b"(?P<minor>\d+)\."
    b"(?P<patch>\d+)"
)


def get_mate_version():
    """
    Return namedtuple with major, minor and patch version of Mate
    or None if Mate is not installed.
    """

    try:
        mate_about_output = subprocess.check_output(
            ("mate-about", "--version")
        )
    except FileNotFoundError:
        return None
    match = pattern.search(mate_about_output)
    return (MateVersion(
        major=int(match.group("major")),
        minor=int(match.group("minor")),
        patch=int(match.group("patch")),
    ))


def import_gtk():
    import gi

    version = get_mate_version()
    if version and version.major < 2 and version.minor < 18:
        gi.require_version("Gtk", "2.0")
    elif version:
        gi.require_version("Gtk", "3.0")
    else:
        # TODO: add logging
        sys.exit(1)
    gi.require_version('MatePanelApplet', '4.0')

