"""
"""
import sys

from luna.w_objects import W_Pri, W_Num
from luna.module import ModuleDef
from luna.modules.patterns import find, build_expr


StringModule = ModuleDef('string')


@StringModule.function('find')
def method_find(args):
    start = 0
    plain = False

    if len(args) > 2:
        start = args[2].n_val - 1
        if len(args) > 3:
            w_pri = args[3]
            assert isinstance(w_pri, W_Pri)
            plain = w_pri.is_true()

    expr = build_expr(args[1].s_val, plain)
    matches = find(expr, args[0].s_val, start)
    if matches == (-1, -1):
        return [W_Pri(0)]
    else:
        return [W_Num(matches[0]), W_Num(matches[1])]
