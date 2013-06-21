"""
Implementation of Lua's table functions
http://www.lua.org/manual/5.1/manual.html#5.5
"""
from pylua.w_objects import W_Table, W_Str, W_Pri
from pylua.module import ModuleDef


TableModule = ModuleDef('table')


@TableModule.function('concat')
def method_concat(args):
    assert isinstance(args[0], W_Table)
    assert isinstance(args[1], W_Str)
    strs = [x.to_str() for x in args[0].content.itervalues() if not(isinstance(x, W_Pri) and x.n_val == 0)]
    s = args[1].s_val.join(strs)
    return W_Str(s)
