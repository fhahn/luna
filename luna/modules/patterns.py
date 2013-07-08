"""
Lua pattern matcher

inspired by
http://morepypy.blogspot.com/2010/05/efficient-and-elegant-regular.html
"""


class Pattern(object):
    def __init__(self, empty):
        # empty denotes whether the regular expression
        # can match the empty string
        self.empty = empty
        # mark that is shifted through the regex
        self.marked = False
        self.length = 1

    def shift(self, c, mark):
        """ shift the mark from left to right, matching character c."""
        # _shift is implemented in the concrete classes
        marked = self._shift(c, mark)
        self.marked = marked
        return marked


class Sequence(Pattern):
    def __init__(self, left, right):
        Pattern.__init__(self, False)
        self.left = left
        self.right = right
        self.length = left.length + right.length

    def _shift(self, c, mark):
        old_left = self.left.marked
        self.left.shift(c, mark)
        right_marked = self.right.shift(c, mark)
        return old_left and right_marked


class CharRange(Pattern):
    def __init__(self, start, stop):
        Pattern.__init__(self, False)
        self.start = start
        self.stop = stop

    def _shift(self, c, mark):
        return mark and (ord(c) >= self.start and ord(c) <= self.stop)


class Char(CharRange):
    def __init__(self,  c):
        CharRange.__init__(self, ord(c), ord(c))


class Dot(Pattern):
    def __init__(self):
        Pattern.__init__(self, False)

    def _shift(self, c, mark):
        return mark


def find(expr, string, start):
    assert isinstance(start, int)
    if start < 0:
        start = len(string) + start
        # if negative offset is bigger than length of string
        # start at the beginning
        if start < 0:
            start = 0
        start = int(start)
    assert start >= 0
    for i in xrange(start, len(string)):
        if expr.shift(string[i], True):
            return i-expr.length+2, i+1
    return -1, -1


SPECIAL_CHARS = {
    'a': (ord('A'), ord('z'))
}

def build_expr(pattern, plain):
    expr = None
    seq = False
    if plain:
        raise RuntimeError('Plain not implemented at the moment')

    new_expr = None
    i = 0
    while i < len(pattern):
        c = pattern[i]
        if c == '.':
            new_expr = Dot()
        elif ord(c) >= ord('0') and ord(c) <= ord('z'):
            new_expr = Char(c)
        elif c == '%':
            i += 1
            c = pattern[i]
            if c == '%':
                new_expr = Char('%')
            elif c in SPECIAL_CHARS:
                new_expr = CharRange(*SPECIAL_CHARS[c])
            else:
                assert 0
        else:
            assert 0
        if seq:
            expr = Sequence(expr, new_expr)
        else:
            expr = new_expr
        seq = True
        i += 1

    return expr
