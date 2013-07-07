from luna.objspace import ObjectSpace
from luna.helpers import debug_print


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
