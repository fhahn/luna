from pylua.w_objects import W_Object

from pylua.modules.builtin import Builtin
from pylua.modules.table import TableModule
from pylua.modules.lmath import MathModule


class ObjectSpace(object):
    def __init__(self):
        self.globals = {}
        self.modules = {}
        self.registers = [W_Object()] * 10
        self.globals.update(Builtin.methods)
        self.add_module(TableModule)
        self.add_module(MathModule)

    def add_module(self, moduledef):
        self.globals[moduledef.name] = moduledef.methods
        self.modules[moduledef.name] = moduledef
