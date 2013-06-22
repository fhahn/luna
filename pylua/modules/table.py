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

    num_args = len(args)
    if num_args > 1:
        assert isinstance(args[1], W_Str)
        sep = args[1].s_val
    else:
        sep = ''

    i = 0
    j = None
    if num_args > 2:
        i = args[2].n_val
    if num_args == 4:
        j = args[3].n_val + 1

    if j is None:
        values = args[0].content.values()[i:]
    else:
        values = args[0].content.values()[i:j]
    strs = [x.to_str() for x in values
            if not(isinstance(x, W_Pri) and x.n_val == 0)]
    s = sep.join(strs)
    return W_Str(s)
