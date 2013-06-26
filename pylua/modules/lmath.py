"""
Implementation of Lua's mathematical functions
"""
import sys
from math import floor

from pylua.w_objects import W_Num
from pylua.module import ModuleDef


MathModule = ModuleDef('math')
MathModule.add_constant('huge', W_Num(sys.maxint))


@MathModule.function('floor')
def method_floor(args):
    return [W_Num(floor(args[0].n_val))]
