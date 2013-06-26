from pylua.objspace import ObjectSpace
from pylua.luaframe import LuaBuiltinFrame
from pylua.helpers import debug_print


class Interpreter(object):
    def __init__(self, flags, root_frame):
        self.flags = flags
        self.root_frame = root_frame

    def run(self):
        returnvalue = None
        space = ObjectSpace()

        returnvalue = self.root_frame.execute_frame(space)

        debug_print("Finished intepreting")
        return returnvalue[0]
