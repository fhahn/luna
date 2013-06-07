from pylua.objspace import ObjectSpace
from pylua.luaframe import LuaBuiltinFrame
from pylua.helpers import debug_print


"""
prints arg to std out
"""
def m_print(arg):
    print(arg.to_str())


class Interpreter(object):
    def __init__(self, flags, root_frame):
        self.flags = flags
        self.root_frame = root_frame

    def run(self):
        returnvalue = None
        space = ObjectSpace()
        # register a global print function, only works with one argument at the
        # moment and is a hack
        space.globals['print'] = LuaBuiltinFrame(m_print)

        returnvalue = self.root_frame.execute_frame(space)

        debug_print("Finished intepreting")
        return returnvalue
