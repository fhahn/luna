"""
Implementation of Lua's basic functions
http://www.lua.org/manual/5.1/manual.html#5.1
"""
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
