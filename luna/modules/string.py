"""
"""
import sys

from luna.w_objects import W_Pri, W_Num, W_Str
from luna.module import ModuleDef
from luna.modules.patterns import find, build_expr


StringModule = ModuleDef('string')


def handle_args(args):
    s = args[0].s_val
    start = 0
    plain = False
    expr = build_expr(args[1].s_val, plain)

    if len(args) > 2:
        start = args[2].n_val - 1
        if len(args) > 3:
            w_pri = args[3]
            assert isinstance(w_pri, W_Pri)
            plain = w_pri.is_true()
    return s, expr, start, plain


@StringModule.function('find')
def method_find(args):
    s, expr, start, plain = handle_args(args)
    matches = find(expr, s, start)
    if matches == (-1, -1):
        return [W_Pri(0)]
    else:
        return [W_Num(matches[0]), W_Num(matches[1])]


@StringModule.function('match')
def method_match(args):
    s, expr, start, plain = handle_args(args)
    start_i, stop_i = find(expr, s, start)
    if (start_i, stop_i) == (-1, -1):
        return [W_Pri(0)]
    else:
        return [W_Str(s[start_i-1:stop_i])]
