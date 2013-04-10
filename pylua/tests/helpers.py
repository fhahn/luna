import os
import tempfile

from pylua.bytecode import Parser
from pylua.interpreter import Interpreter


def codetest(src_text):
    f = tempfile.NamedTemporaryFile()
    f.write(src_text)
    f.flush()
    ret = os.system('luajit -b %s %s' %(f.name, f.name+'c'))
    if ret:
        raise RuntimeError("Compilation failed")
    flags, protos = Parser(f.name+'c').parse()
    interpreter = Interpreter(flags, protos)
    ret = interpreter.run()
    return ret
