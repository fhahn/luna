from luna.w_objects import W_Object

from luna.modules.builtin import Builtin
from luna.modules.table import TableModule
from luna.modules.lmath import MathModule
from luna.modules.string import StringModule


class ObjectSpace(object):
    def __init__(self):
        self.globals = {}
        self.modules = {}
        self.registers = [W_Object()] * 10
        self.globals.update(Builtin.methods)
        self.add_module(TableModule)
        self.add_module(MathModule)
        self.add_module(StringModule)

    def add_module(self, moduledef):
        self.globals[moduledef.name] = moduledef.methods
        self.modules[moduledef.name] = moduledef
