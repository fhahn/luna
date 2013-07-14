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
        self.matched = 0, 0

    def shift(self, c, mark):
        """ shift the mark from left to right, matching character c."""
        # _shift is implemented in the concrete classes
        self.matched = self._shift(c, mark)
        return self.matched


class Sequence(Pattern):
    def __init__(self, left, right):
        Pattern.__init__(self, False)
        self.left = left
        self.right = right

    def _shift(self, c, mark):
        old_left = self.left.matched
        self.left.shift(c, mark)
        right_matched = self.right.shift(c, mark)
        if old_left[0] != 0 and right_matched[0] != 0:
            new_matched = (old_left[0] + right_matched[0], old_left[1] + right_matched[1])
            if new_matched[0] == 0:
                return 1, new_matched[1]
            return new_matched
        return 0, 0


class CharRange(Pattern):
    def __init__(self, start, stop):
        Pattern.__init__(self, False)
        self.start = start
        self.stop = stop

    def _shift(self, c, mark):
        if mark and (ord(c) >= self.start and ord(c) <= self.stop):
            return 1, 0
        else:
            return 0, 0


class Char(CharRange):
    def __init__(self,  c):
        CharRange.__init__(self, ord(c), ord(c))


class Dot(Pattern):
    def __init__(self):
        Pattern.__init__(self, False)

    def _shift(self, c, mark):
        return mark, 0


class Star(Pattern):
    def __init__(self, token):
        Pattern.__init__(self, False)
        self.token = token
        self.num_matched = 0

    def _shift(self, c, mark):
        new_matched = self.token.shift(c, mark)
        if self.num_matched == 0 and new_matched[0] == 0:
            return -1, 1
        elif self.num_matched > 0 and new_matched[0] == 0:
            return self.num_matched, 1
        else:
            self.num_matched += 1
            return 0, 0


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
        matched, greedy = expr.shift(string[i], True)
        if matched == -1:
            return i+1, i
        elif matched > 0:
            m_start = i-matched+2-greedy
            return m_start, i+1-greedy
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
