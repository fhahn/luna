from pylua.objspace import ObjectSpace
from pylua.luaframe import LuaBuiltinFrame, SReturnValue
from pylua.helpers import debug_print
from pylua.bytecode import Constant

"""
prints arg to std out
"""
def m_print(arg):
    print(arg)

class Interpreter(object):
    def __init__(self, flags, frames):
        self.flags = flags
        self.frames = frames
        self.num_frames = len(frames)

    def run(self):
        returnvalue = None
        space = ObjectSpace()
        # register a global print function, only works with one argument at the
        # moment and is a hack
        space.globals['print'] = Constant(f_val=LuaBuiltinFrame(m_print))
        while True:
            frame_ind = 0
            next_frame = self.frames[frame_ind]
            frame_ind += 1

            returnvalue = next_frame.execute_frame(space)
            if frame_ind == self.num_frames or returnvalue is not None:
                break

        debug_print("Finished intepreting")
        return returnvalue
