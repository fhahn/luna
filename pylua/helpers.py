DEBUG = False


def debug_print(args):
    if DEBUG:
        print(args)


# TODO: is there a better way to save different types in the constants list
class Constant(object):
    _immutable_ = True

    def __init__(self, s_val="", n_val=0, f_val=None):
        self.s_val = s_val
        self.n_val = n_val
        self.f_val = f_val

    def getval(self):
        return self.val
