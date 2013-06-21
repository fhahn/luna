from pylua.luaframe import LuaBuiltinFrame
from pylua.w_objects import W_Table


class ModuleDef(object):
    def __init__(self, name):
        self.name = name
        self.methods = W_Table()

    def function(self, name):
        def adder(func):
            self.methods.content[name] = LuaBuiltinFrame(func)
        return adder
