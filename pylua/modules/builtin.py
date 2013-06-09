"""
Implementation of Lua's basic functions
http://www.lua.org/manual/5.1/manual.html#5.1
"""

from pylua.module import ModuleDef


Builtin = ModuleDef('Builtin')


@Builtin.function('print')
def method_print(args):
    args = ' '.join([x.to_str() for x in args])
    print args
