"""
Lua pattern matcher based on a NFA

inspired by
http://swtch.com/~rsc/regexp/regexp1.html
"""


 
class State(object):
    pass


class StateMatch(State):
    def __init__(self):
        pass


class StateCharRange(State):
    def __init__(self, c1, c2, out):
        self.start = ord(c1)
        self.stop = ord(c2)
        self.out = out

    def match(self, c):
        return ord(c) >= self.start and  ord(c) <=self.stop


class StateChar(StateCharRange):
    def __init__(self, c, out):
        StateCharRange.__init__(self, c, c, out)

class StateDot(StateCharRange):
    def __init__(self, out):
        StateCharRange.__init__(self, ' ', ' ' , out)

    def match(self, c):
        return True


class StateSplit(State):
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
    prev = expr
 
    assert isinstance(pattern, str)
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
