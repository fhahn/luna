"""
Implementation of Lua's basic functions
http://www.lua.org/manual/5.1/manual.html#5.1
"""
import os

from luna.bytecode import Parser
from luna.w_objects import W_Num, W_Pri, W_Str, W_Table
from luna.luaframe import LuaFrame
from luna.module import BuiltinDef


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
    os.system('luajit -b %s %s' %(filename, filename+'c'))
    flags, protos = Parser(filename+'c').parse()
    return [protos]


@Builtin.function('loadstring')
def method_loadstring(args):
    s = args[0].s_val
    i = 0
    filename = ''
    name_tpl= '/tmp/luna'
    while True:
        filename = "".join([name_tpl, str(i), ".lua"])
        if not os.path.exists(filename):
            break
        i += 1
    fd = os.open(filename, os.O_WRONLY|os.O_CREAT, 0777)
    os.write(fd, s)
    os.close(fd)
    os.system('luajit -b %s %s' %(filename, filename+'c'))
    os.remove(filename)
    flags, protos = Parser(filename+'c').parse()
    return [protos]


@Builtin.function('tonumber')
def method_tonumber(args):
    if len(args) > 1:
        raise RuntimeError("tonumber with base not supported at the moment")
    try:
        return [W_Num(float(args[0].s_val))]
    except ValueError:
        return [W_Pri(0)]


@Builtin.function('type')
def method_type(args):
    w_obj = args[0]
    t = ""
    if isinstance(w_obj, W_Pri):
        t = 'boolean'
    elif isinstance(w_obj, W_Num):
        t = "number"
    elif isinstance(w_obj, W_Str):
        t = 'string'
    elif isinstance(w_obj, W_Table):
        t = 'table'
    elif isinstance(w_obj, LuaFrame):
        t = 'function'
    else:
        raise RuntimeError('Unsupported type')
    return [W_Str(t)]
