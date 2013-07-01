import sys
import os

from rpython.translator.goal.translate import main


if __name__ == "__main__":
    root_dir = os.path.abspath(__file__)
    sys.argv = [arg for arg in
                sys.argv + ['--output', 'lunac', os.path.join('luna/main')]]
    main()
