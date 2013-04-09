import sys
import os

from pylua.bytecode import Parser
from pylua.interpreter import Interpreter


def _needs_compilation(path1, path2):
    """Checks if path1 exists and is up to date or need to be compiled."""
    try:
        f1_mtime = os.stat(path1).st_mtime
        if f1_mtime < os.stat(path2).st_mtime:
            return True
    except OSError:
        return True
    return False

def main(argv):
    try:
        filename = argv[1]
    except IndexError:
        print "You must supply a filename"
        print (argv)
        return 1

    file_, ext = argv[1].rsplit('.', 1)
    if ext not in ('l', 'lc'):
    	print("Unsupported extension %s" %ext)
    	return 1

    if _needs_compilation(file_+'.lc', filename):
    	ret = os.system('luajit -b %s %s' %(filename, filename+'c'))
    	if ret:
    		print("Error compiling %s using luajit" % filename)
    		return 1

    if ext == 'l':
    	filename += 'c'
    flags, protos = Parser(filename).parse()
    interpreter = Interpreter(flags, protos)
    interpreter.run()
    
    return 0

def target(*args):
    return main, None

if __name__ == "__main__":
    main(sys.argv)