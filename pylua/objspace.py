from pylua.w_objects import W_Object

class ObjectSpace(object):
    def __init__(self):
        self.globals = {}
        self.registers = [W_Object()] * 10
