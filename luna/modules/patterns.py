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
        return ord(c) >= self.start and ord(c) <= self.stop


class StateChar(StateCharRange):
    def __init__(self, c, out):
        StateCharRange.__init__(self, c, c, out)


class StateDot(StateCharRange):
    def __init__(self, out):
        StateCharRange.__init__(self, ' ', ' ', out)

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
            if (isinstance(state, StateMatch) or
                    (isinstance(state, StateSplit) and
                        isinstance(state.out2, StateMatch))):
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


def set_next(state, next_state, propagate=False):
    if isinstance(state, StateSplit):
        if state.out is None:
            state.out = next_state
        elif state.out2 is None:
            state.out2 = next_state
        elif propagate:
                set_next(state.out, next_state)
                set_next(state.out2, next_state)
    else:
        if state.out is None:
            state.out = next_state
        elif propagate:
            set_next(state.out, next_state)


T_CHAR = 0
T_DOT = 1
T_CHAR_RANGE = 2
T_STAR = 3
T_OR = 4


class Token(object):
    def __init__(self, t_type, value, sub_tokens=[], tokens_right=[]):
        self.type = t_type
        self.value = value
        self.sub_tokens = sub_tokens
        self.tokens_right = tokens_right


def tokenize(pattern):
    tokens = []

    i = 0
    while i < len(pattern):
        c = pattern[i]
        if ord(c) >= ord('0') and ord(c) <= ord('z'):
            tokens.append(Token(T_CHAR, [c]))
        elif c == '.':
            tokens.append(Token(T_DOT, [c]))
        elif c == '%':
            if i+1 < len(pattern):
                if pattern[i+1] == '%':
                    tokens.append(Token(T_CHAR, ['%']))
                elif pattern[i+1] in SPECIAL_CHARS:
                    tokens.append(
                        Token(T_CHAR_RANGE, list(SPECIAL_CHARS[pattern[i+1]]))
                    )
                else:
                    raise RuntimeError('Invalid pattern')
                i += 1
            else:
                raise RuntimeError('Invalid pattern')
        elif c == '*':
            if len(tokens) > 0:
                prev = tokens.pop()
                tokens.append(Token(T_STAR, [], sub_tokens=[prev]))
            else:
                raise RuntimeError('Invalid pattern')
        elif c == '|':
            tokens_right = tokenize(pattern[i+1:])
            return [
                Token(T_OR, [], sub_tokens=tokens, tokens_right=tokens_right)
            ]
        else:
            raise RuntimeError('Invalid pattern')
        i += 1
    return tokens


def tokens_to_expression(tokens, top=True):
    expr = StateChar('c', None)
    start = expr
    for t in tokens:
        new_expr = None
        if t.type == T_CHAR:
            new_expr = StateChar(t.value[0], None)
        elif t.type == T_DOT:
            new_expr = StateDot(None)
        elif t.type == T_CHAR_RANGE:
            new_expr = StateCharRange(t.value[0], t.value[1], None)
        elif t.type == T_STAR:
            match_expr = tokens_to_expression(t.sub_tokens, top=False)
            new_expr = StateSplit(match_expr, None)
            set_next(match_expr, new_expr)
        elif t.type == T_OR:
            expr_left = tokens_to_expression(t.sub_tokens, top=False)
            expr_right = tokens_to_expression(t.tokens_right, top=False)
            new_expr = StateSplit(expr_left, expr_right)
        set_next(expr, new_expr)
        expr = new_expr
    if top:
        set_next(expr, StateMatch(), propagate=True)
    return start.out


def compile_re(pattern, plain=False):
    tokens = tokenize(pattern)
    return tokens_to_expression(tokens)
