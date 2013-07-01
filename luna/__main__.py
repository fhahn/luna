import sys

from luna.main import create_entry_point

entry_point = create_entry_point()
sys.exit(entry_point(sys.argv))
