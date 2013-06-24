"""
Implementation of Lua's basic functions
http://www.lua.org/manual/5.1/manual.html#5.1
"""
import os 

from pylua.bytecode import Parser
from pylua.w_objects import W_Num, W_Pri, W_Str
from pylua.module import BuiltinDef


Builtin = BuiltinDef('Builtin')


@Builtin.function('assert')
def method_assert(args):
    # TODO return all arguments
    if len(args) == 2:
        msg = args[1].to_str()
    else:
        msg = 'assertion failed'

    if ((isinstance(args[0], W_Pri) and args[0].n_val != 2) or
        (isinstance(args[0], W_Num) and args[0].n_val == 0)):
            raise AssertionError(msg)


@Builtin.function('print')
def method_print(args):
    args = ' '.join([x.to_str() for x in args])
    print args


@Builtin.function('loadfile')
def method_loadfile(args):
    filename = args[0].s_val
    ret = os.system('luajit -b %s %s' %(filename, filename+'c'))
    flags, protos = Parser(filename+'c').parse()
    return protos


@Builtin.function('loadfile')
def method_loadfile(args):
    filename = args[0].s_val
    ret = os.system('luajit -b %s %s' %(filename, filename+'c'))
    flags, protos = Parser(filename+'c').parse()
    return protos


@Builtin.function('tonumber')
def method_tonumber(args):
    if len(args) > 1:
        raise RuntimeError("tonumber with base not supported at the moment")
    try:
        return W_Num(float(args[0].s_val))
    except ValueError:
        return W_Pri(0)
