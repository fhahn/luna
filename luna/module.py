from luna.luaframe import LuaBuiltinFrame
from luna.w_objects import W_Table, W_Str


class ModuleDef(object):
    def __init__(self, name):
        self.name = name
        self.methods = W_Table()

    def function(self, name):
        def adder(func):
            self.methods.set(W_Str(name), LuaBuiltinFrame(func))
        return adder

    def add_constant(self, name, w_const):
        self.methods.set(W_Str(name), w_const)


class BuiltinDef(object):
    def __init__(self, name):
        self.name = name
        self.methods = {}

    def function(self, name):
        def adder(func):
            self.methods[name] = LuaBuiltinFrame(func)
        return adder
