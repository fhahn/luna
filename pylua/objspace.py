from pylua.w_objects import W_Object

from pylua.modules.builtin import Builtin
from pylua.modules.table import TableModule


class ObjectSpace(object):
    def __init__(self):
        self.globals = {}
        self.modules = {}
        self.registers = [W_Object()] * 10
        self.add_module(Builtin)
        self.add_module(TableModule)

    def add_module(self, moduledef):
        if moduledef.name == "Builtin":
            self.globals.update(moduledef.methods.content)
        else:
            self.globals[moduledef.name] = moduledef.methods

        self.modules[moduledef.name] = moduledef
