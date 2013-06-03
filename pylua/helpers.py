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
        raise NotImplementedError('eq not supported by this class')

    def neq(self, w_other):
        raise NotImplementedError('neq not supported by this class')

    def gt(self, other):
        raise NotImplementedError('gt not supported by this class')

    def lt(self, other):
        raise NotImplementedError('lt not supported by this class')

    def ge(self, other):
        raise NotImplementedError('ge not supported by this class')

    def le(self, other):
        raise NotImplementedError('le not supported by this class')

    def to_str(self):
        raise NotImplementedError('to_str not supported by this class')

    def clone(self):
        raise NotImplementedError('to_str not supported by this class')


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

    def gt(self, w_other):
        assert isinstance(w_other, W_Num)
        return self.n_val > w_other.n_val

    def lt(self, w_other):
        assert isinstance(w_other, W_Num)
        return self.n_val < w_other.n_val

    def le(self, w_other):
        assert isinstance(w_other, W_Num)
        return self.n_val <= w_other.n_val

    def ge(self, w_other):
        assert isinstance(w_other, W_Num)
        return self.n_val >= w_other.n_val

    def to_str(self):
        return str(self.n_val)

    def clone(self):
        return W_Num(self.n_val)


class W_Str(W_Object):
    def __init__(self, val):
        self.s_val = val
        self.type = 'STR'

    def getval(self):
        return self.s_val

    def eq(self, w_other):
        assert isinstance(w_other, W_Str)
        return self.s_val == w_other.getval()

    def neq(self, w_other):
        return not self.eq(w_other)

    def gt(self, w_other):
        assert isinstance(w_other, W_Str)
        return self.s_val > w_other.s_val

    def lt(self, w_other):
        assert isinstance(w_other, W_Str)
        return self.s_val < w_other.s_val

    def le(self, w_other):
        assert isinstance(w_other, W_Str)
        return self.s_val <= w_other.s_val

    def ge(self, w_other):
        assert isinstance(w_other, W_Str)
        return self.s_val >= w_other.s_val

    def to_str(self):
        return str(self.s_val)

    def clone(self):
        return W_Str(self.s_val)


class W_Func(W_Object):
    def __init__(self, val):
        self.f_val = val
        self.type = 'STR'

    def getval(self):
        return self.f_val

    def clone(self):
        return W_Func(self.f_val)


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
