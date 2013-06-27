"""
Implementation of Lua's table functions
http://www.lua.org/manual/5.1/manual.html#5.5
"""
from pylua.w_objects import W_Table, W_Str, W_Pri, W_Num
from pylua.module import ModuleDef


TableModule = ModuleDef('table')


@TableModule.function('concat')
def method_concat(args):
    assert isinstance(args[0], W_Table)
    w_table = args[0]

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
        values = w_table.values()[i:]
    else:
        values = w_table.values()[i:j]
    strs = [x.to_str() for x in values
            if not(isinstance(x, W_Pri) and x.n_val == 0)]
    s = sep.join(strs)
    return [W_Str(s)]


@TableModule.function('insert')
def method_insert(args):
    assert isinstance(args[0], W_Table)
    w_table = args[0]
    num_args = len(args)
    if num_args == 2:
        args[0].set(W_Num(w_table.size()), args[1])
    elif num_args == 3:
        pos = args[1]
        items = list(w_table.items())
        i = len(items) - 1
        while i >= pos.n_val:
            k, v = items[i]
            k += 1
            w_table.set(W_Num(k), v)
            i -= 1
        w_table.set(pos, args[2])
    else:
        assert 0


@TableModule.function('maxn')
def method_maxn(args):
    raise NotImplementedError("table.maxn not implemented")


@TableModule.function("remove")
def method_remove(args):
    assert isinstance(args[0], W_Table)
    w_table = args[0]
    assert isinstance(args[1], W_Num)
    pos = args[1]

    elem = None
    if pos.n_val < w_table.size() and pos.n_val > 0:
        elem = w_table.get(pos)
    else:
        return [W_Pri(0)]

    items = list(w_table.items())

    i = pos.n_val
    assert isinstance(i, int)
    while (i+1) < len(items):
        k, v = items[i+1]
        k -= 1
        w_table.set(W_Num(k), v)
        i += 1
    del w_table.content[items[-1][0]]
    return [elem]
