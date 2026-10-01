import os
import signal
import sys

signal.signal(signal.SIGPIPE, signal.SIG_DFL)  # ./bib find | head

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bib.cli import main  # noqa: E402

sys.exit(main())
