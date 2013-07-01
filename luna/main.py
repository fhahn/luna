import os

from luna.bytecode import Parser
from luna.interpreter import Interpreter


def _needs_compilation(path1, path2):
    """Checks if path1 exists and is up to date or need to be compiled."""
    try:
        f1_mtime = os.stat(path1).st_mtime
        if f1_mtime < os.stat(path2).st_mtime:
            return True
    except OSError:
        return True
    return False


def create_entry_point():
    def entry_point(argv):
        try:
            filename = argv[1]
        except IndexError:
            print "You must supply a filename"
            print (argv)
            return 1

        file_, ext = argv[1].rsplit('.', 1)
        """
        if ext not in ('l', 'lc'):
            print("Unsupported extension %s" %ext)
            return 1
        """

        if _needs_compilation(file_+'.lc', filename):
            ret = os.system('luajit -b %s %s' %(filename, filename+'c'))
            if ret:
                print("Error compiling %s using luajit" % filename)
                return 1

        if not ext.endswith('c'):
            filename += 'c'

        flags, protos = Parser(filename).parse()
        interpreter = Interpreter(flags, protos)
        interpreter.run()

        return 0
    return entry_point


def target(driver, args):
    return create_entry_point(), None
