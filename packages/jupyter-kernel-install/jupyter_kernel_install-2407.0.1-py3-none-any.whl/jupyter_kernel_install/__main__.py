"""Command line interface for jupyter_kernel_install."""

import re
import sys

from .cli import cli

if __name__ == "__main__":
    sys.argv[0] = re.sub(r"(-script\.pyw|\.exe)?$", "", sys.argv[0])
    cli(sys.argv[1:])
