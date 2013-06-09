from pylua.luaframe import LuaBuiltinFrame



class ModuleDef(object):
    def __init__(self, name):
        self.name = name
        self.methods = {}

    def function(self, name):
        def adder(func):
            self.methods[name] = LuaBuiltinFrame(func)
        return adder
