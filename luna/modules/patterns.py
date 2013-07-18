"""
Lua pattern matcher based on a NFA

inspired by
http://swtch.com/~rsc/regexp/regexp1.html
"""


class Pattern(object):
    def __init__(self, empty):
        # empty denotes whether the regular expression
        # can match the empty string
        self.empty = empty
        # mark that is shifted through the regex
        self.matched = False, 0

    def shift(self, mark, c1, c2=''):
        """ shift the mark from left to right, matching character c."""
        # _shift is implemented in the concrete classes
        self.matched = self._shift(mark, c1, c2)
        return self.matched

    def eq(self, other):
        return type(self) == type(other)

    def reset(self):
        self.matched = False, 0


class Sequence(Pattern):
    def __init__(self, left, right):
        Pattern.__init__(self, False)
        self.left = left
        self.right = right

    def _shift(self, mark, c1, c2):
        old_left = self.left.matched
        marked_left = self.left.shift(mark, c1, c2)
        marked_right = self.right.shift(old_left or (mark and self.left.empty), c1, c2)
        if marked_left[0] and self.right.empty:
            return True, marked_left[1]
        if marked_right[0]:
            return True, marked_right[1]
        return False, 0

    def eq(self, other):
        t_eq = Pattern.eq(self, other)
        # left and right should never be None
        return t_eq and self.left.eq(other.left) and self.right.eq(other.right)

    def reset(self):
        self.left.reset()
        self.right.reset()


class CharRange(Pattern):
    def __init__(self, start, stop):
        Pattern.__init__(self, False)
        self.start = start
        self.stop = stop

    def _shift(self, mark, c1, c2):
        if len(c1) == 0:
            return False, 0
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


class StateMatch(object):
    def __init__(self):
        pass


class StateCharRange(object):
    def __init__(self, c1, c2, out):
        self.start = ord(c1)
        self.stop = ord(c2)
        self.out = out

    def match(self, c):
        return self.start >= ord(c) and self.stop <= ord(c)


class StateChar(StateCharRange):
    def __init__(self, c, out):
        StateCharRange.__init__(self, c, c, out)

class StateDot(StateCharRange):
    def __init__(self, out):
        StateCharRange.__init__(self, ' ', ' ' , out)

    def match(self, c):
        return True


class StateSplit(object):
    def __init__(self, out, out2):
        self.out = out
        self.out2 = out2


def find2(expr, string, start):
    assert isinstance(start, int)
    if start < 0:
        start = len(string) + start
        # if negative offset is bigger than length of string
        # start at the beginning
        if start < 0:
            start = 0
        start = int(start)

    found = False
    i = start
    while i < len(string):
        match = False
        valid = True
        j = i
        state = expr
        backtrack = []
        while valid and not match and j < len(string):
            if isinstance(state, StateCharRange):
                if not state.match(string[j]):
                    if len(backtrack) == 0:
                        valid = False
                    else:
                        state, j = backtrack.pop()
                else:
                    state = state.out
                    j += 1
            elif isinstance(state, StateMatch):
                match = True
            elif isinstance(state, StateSplit):
                backtrack.append((state.out2, j))
                state = state.out
            else: 
                valid = False
        if j == len(string):
            if (isinstance(state, StateSplit) and isinstance(state.out2, StateMatch)) or isinstance(state, StateMatch):
                match = True

        if match:
            found = True
            yield (i+1, j)
            if j > i:
                i = j
            else:
                i += 1
        else:
            i += 1
    if not found:
        yield (-1, -1)



class Star(Pattern):
    def __init__(self, re):
        Pattern.__init__(self, True)
        self.re = re
        self.num_matched = 0

    def _shift(self, mark, c1, c2):
        matched = self.re.shift(mark, c1, c2)
        next_matched = self.re.shift(mark, c2, c2)
        if not matched[0]:
            return True, 0
        elif self.num_matched > 0 and next_matched[0] == 0:
            matched = self.num_matched + 1
            self.num_matched = 0
            return True, matched
        elif not next_matched[0]:
            return True, 1
        else:
            self.num_matched += 1
            self.empty = False
            return False, 0

    def eq(self, other):
        t_eq = Pattern.eq(self, other)
        # re should never be None
        return t_eq and self.re.eq(other.re)

    def reset(self):
        Pattern.reset(self)
        self.num_matched = 0


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
    found = False
    match_count = -1
    mark = True
    for i in xrange(start, len(string)-1):
        matched, count = expr.shift(mark, string[i], string[i+1])
        if (not matched or count == match_count) and match_count >= 0:
            if match_count == 0:
                yield (i+1, i)
            else:
                m_start = i-match_count+2
                yield (m_start, i+1)
            found = True
            expr.reset()
            match_count = -1
        if matched:
            match_count = count

    i = len(string) - 1
    matched, count = expr.shift(True, string[i])

    if not matched and match_count >= 0:
        i -= 1
        if match_count == 0:
            yield (i+1, i)
        else:
            m_start = i-match_count+2
            yield (m_start, i+1)
        found = True
        expr.reset()

    if matched:
        if count == 0:
            yield (i+1, i)
        else:
            m_start = i-count+2
            yield (m_start, i+1)
        found = True
        expr.reset()


    if not found:
        yield (-1, -1)


SPECIAL_CHARS = {
    'a': ('A', 'z')
}


def set_next(state, next_state):
    if isinstance(state, StateSplit):
        if state.out is None:
            state.out = next_state
        else:
            state.out2 = next_state
    else:
        state.out = next_state


def build_expr(pattern, plain):
    expr = None
    if plain:
        raise RuntimeError('Plain not implemented at the moment')

    expr = StateChar('c', None)
    prev = None
    start = expr
    i = 0
    prev = [expr,]
 
    while i < len(pattern):
        c = pattern[i]
        if c == '.':
            new_expr = StateDot(None)
            set_next(expr, new_expr)
            path = 1
        elif ord(c) >= ord('0') and ord(c) <= ord('z'):
            new_expr = StateChar(c, None)
            set_next(expr, new_expr)
            path = 1
        elif c == '%':
            i += 1
            c = pattern[i]
            if c == '%':
                new_expr = StateChar('%', None)
                expr.out = new_expr
            elif c in SPECIAL_CHARS:
                new_expr = StateCharRange(SPECIAL_CHARS[c][0], SPECIAL_CHARS[c][1], None)
                expr.out = new_expr
            else:
                assert 0
            set_next(expr, new_expr)
            path = 1
        elif c == '*':
            new_expr = StateSplit(expr, None)
            set_next(prev, new_expr)
            set_next(expr, new_expr)
            path = 2
            prev_path = 2
        else:
            assert 0
        prev = expr
        expr = new_expr
        i += 1

    set_next(expr, StateMatch())

    return start.out
