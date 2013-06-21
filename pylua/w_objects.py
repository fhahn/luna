from rpython.rlib.objectmodel import compute_hash, compute_identity_hash


class W_Object(object):
    def __init__(self):
        self.n_val = 0
        self.s_val = ''
        self.content = {}

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
        raise NotImplementedError('clone not supported by this class')

    def get_val(self, key):
        raise NotImplementedError('to_str not supported by this class')

    def hash(self):
        raise NotImplementedError('hash not supported by this class')


class W_Num(W_Object):
    def __init__(self, val):
        self.n_val = val

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

    def hash(self):
        return self.n_val


class W_Str(W_Object):
    def __init__(self, val):
        self.s_val = val

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

    def hash(self):
        return compute_hash(self.s_val)


class W_Func(W_Object):
    def __init__(self, val):
        self.f_val = val

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

    def clone(self):
        return W_Pri(self.n_val)


class W_Table(W_Object):
    def __init__(self):
        self.content = {}

    def get_val(self, key):
        try:
            w_v = self.content[key.hash()]
            assert isinstance(w_v, W_Object)
            return w_v
        except KeyError:
            return W_Pri(0)

    def set_val(self, key, val):
        self.content[key.hash()] = val

    def clone(self):
        # TODO: deep copy expceted here?
        cpy = W_Table()
        cpy.content = self.content.copy()
        return cpy

    def hash(self):
        return compute_identity_hash(self.content)
