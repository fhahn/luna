import os
import tempfile

from pylua.bytecode import Parser
from pylua.interpreter import Interpreter


def test_file(src='', suffix=''):
    f = tempfile.NamedTemporaryFile(suffix=suffix)
    f.write(src)
    f.flush()
    return f

def compile_file(f):
    ret = os.system('luajit -b %s %s' %(f.name, f.name+'c'))
    if ret:
        raise RuntimeError("Compilation failed")

def luabytecode_file(src):
    f = test_file(src, suffix='.l')
    compile_file(f)
    return open(f.name+'c')

def codetest(src):
    f = luabytecode_file(src)
    flags, protos = Parser(f.name).parse()
    interpreter = Interpreter(flags, protos)
    ret = interpreter.run()
    return ret
