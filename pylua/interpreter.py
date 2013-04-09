from pylua.instructions import AbstractInstruction

class Interpreter(object):
    def __init__(self, flags, protos):
        self.flags = flags
        self.protos = protos
        self.pc = 0
        self.current_protos = self.protos[0]

    def run(self):
        while True:
            next_inst = self.current_protos.instructions[self.pc]
            self.pc += 1
            ret = next_inst.apply(self)
            if ret == 1:
                break

        print("finished interpreting")
