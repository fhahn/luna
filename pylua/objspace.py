from pylua.w_objects import W_Object

from pylua.modules.builtin import Builtin


class ObjectSpace(object):
    def __init__(self):
        self.globals = {}
        self.modules = {}
        self.registers = [W_Object()] * 10
        self.add_module(Builtin)

    def add_module(self, moduledef):
        self.globals.update(moduledef.methods)
        self.modules[moduledef.name] = moduledef
