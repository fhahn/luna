DEBUG = False


def debug_print(args):
    if DEBUG:
        print(args)


class W_Object(object):
    def __init__(self):
        self.type = 'BASE'
        self.val = None

    def getval(self):
        return self.val

    def eq(self, w_other):
        raise NotImplementedError('eq not implemented in this class')

    def neq(self, w_other):
        raise NotImplementedError('neq not implemented in this clas')

    def to_str(self):
        raise NotImplementedError('to_str not implemented in this class')


class W_Num(W_Object):
    def __init__(self, val):
        self.n_val = val
        self.type = 'NUM'

    def getval(self):
        return self.n_val

    def eq(self, w_other):
        assert isinstance(w_other, W_Num)
        return self.n_val == w_other.getval()

    def neq(self, w_other):
        return not self.eq(w_other)

    def to_str(self):
        return str(self.n_val)


class W_Str(W_Object):
    def __init__(self, val):
        self.s_val = val
        self.type = 'STR'

    def getval(self):
        return self.s_val

    def to_str(self):
        return str(self.s_val)


class W_Func(W_Object):
    def __init__(self, val):
        self.f_val = val
        self.type = 'STR'

    def getval(self):
        return self.f_val

class W_Pri(W_Num):
    def __init__(self, val):
        assert val in (0, 1, 2)
        self.n_val = val

    def to_str(self):
        if self.n_val == 0:
            return 'nil'
        elif self.n_val == 1:
            return 'false'
        else:
            return 'true'
