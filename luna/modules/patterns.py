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

    def shift(self, mark, c1, c2=''):
        """ shift the mark from left to right, matching character c."""
        # _shift is implemented in the concrete classes
        self.matched = self._shift(mark, c1, c2)
        return self.matched

    def eq(self, other):
        return type(self) == type(other)


class Sequence(Pattern):
    def __init__(self, left, right):
        Pattern.__init__(self, False)
        self.left = left
        self.right = right

    def _shift(self, mark, c1, c2):
        old_left = self.left.matched
        marked_left = self.left.shift(mark, c1, c2)
        marked_right = self.right.shift(mark, c1, c2)
        if old_left[0] and marked_right[0]:
            return True, old_left[1] + marked_right[1]
        if marked_left[0] and self.right.empty:
            return True, marked_left[1]
        return False, 0

    def eq(self, other):
        t_eq = Pattern.eq(self, other)
        if self.left:
            l_eq = t_eq and self.left.eq(other.left)
        else:
            l_eq = other.left is None
        if self.right:
            r_eq = t_eq and self.right.eq(other.right)
        else:
            r_eq = other.right is None

        return t_eq and l_eq and r_eq


class CharRange(Pattern):
    def __init__(self, start, stop):
        Pattern.__init__(self, False)
        self.start = start
        self.stop = stop

    def _shift(self, mark, c1, c2):
        if mark and (ord(c1) >= self.start and ord(c1) <= self.stop):
            return True, 1
        else:
            return False, 0

    def eq(self, other):
        t_eq = Pattern.eq(self, other)
        return t_eq and self.start == other.start and self.stop == other.stop


class Char(CharRange):
    def __init__(self,  c):
        CharRange.__init__(self, ord(c), ord(c))


class Dot(Pattern):
    def __init__(self):
        Pattern.__init__(self, False)

    def _shift(self, mark, c1, c2):
        return mark, 1


class Star(Pattern):
    def __init__(self, re):
        Pattern.__init__(self, True)
        self.re = re
        self.num_matched = 0

    def _shift(self, mark, c1, c2):
        matched = self.re.shift(mark, c1, c2)
        next_matched = self.re.shift(mark, c2, c2)
        if self.num_matched == 0 and next_matched[0] == 0:
            return True, 0
        elif self.num_matched > 0 and next_matched[0] == 0:
            matched = self.num_matched+1
            self.num_matched = 0
            return True, matched
        else:
            self.num_matched += 1
            return False, 0

    def eq(self, other):
        t_eq = Pattern.eq(self, other)
        if self.re:
            re_eq = t_eq and self.re.eq(other.re)
        else:
            re_eq = other.re is None
        return t_eq and re_eq


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
    for i in xrange(start, len(string)-1):
        matched, count = expr.shift(True, string[i], string[i+1])
        if matched:
            if count == 0:
                return i+1, i
            m_start = i-count+2
            return m_start, i+1

    i = len(string) - 1
    matched, count = expr.shift(True, string[i])
    if matched:
        m_start = i-count+2
        return m_start, i+1

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

        if i+1 < len(pattern) and pattern[i+1] == '*':
            new_expr = Star(new_expr)
            i += 1

        if seq:
            expr = Sequence(expr, new_expr)
        else:
            expr = new_expr
        seq = True
        i += 1

    return expr
