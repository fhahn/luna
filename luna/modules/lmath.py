"""
Implementation of Lua's mathematical functions
"""
import sys
from math import floor, sin

from luna.w_objects import W_Num
from luna.module import ModuleDef


MathModule = ModuleDef('math')
MathModule.add_constant('huge', W_Num(sys.maxint))


@MathModule.function('floor')
def method_floor(args):
    return [W_Num(floor(args[0].n_val))]


@MathModule.function('sin')
def method_sin(args):
    return [W_Num(sin(args[0].n_val))]

@MathModule.function('mod')
def method_mod(args):
    return [W_Num(args[0].n_val % args[1].n_val)]
