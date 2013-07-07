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


class Char(Pattern):
    def __init__(self,  c):
        Pattern.__init__(self, False)
        self.c = c

    def _shift(self, c, mark):
        return mark and c == self.c


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


def build_expr(pattern, plain):
    expr = None
    seq = False
    if plain:
        raise RuntimeError('Plain not implemented at the moment')

    for c in pattern:
        if ord(c) >= ord('0') and ord(c) <= ord('z'):
            if seq:
                expr = Sequence(expr, Char(c))
            else:
                expr = Char(c)
            seq = True
        else:
            assert 0
    return expr
