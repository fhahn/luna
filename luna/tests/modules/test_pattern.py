from luna.modules.patterns import (
    build_expr, find, Char, Sequence, Dot, CharRange, Star,
    StateMatch, StateOut, find2, StateSplit
)

class TestPattern2(object):
    def test_single_char_no_match(self):
        expr = StateOut('c', StateMatch())
        result = find2(expr, 'xyz', 0)
        assert list(result) == [(-1, -1)]

    def test_single_char_one_match(self):
        expr = StateOut('c', StateMatch())
        result = find2(expr, 'asdasdxcz', 0)
        assert list(result) == [(8, 8)]

    def test_single_char_more_matches(self):
        expr = StateOut('c', StateMatch())
        result = find2(expr, 'xyzaaaccaa', 0)
        assert list(result) == [(7, 7), (8, 8)]

    def test_two_chars_no_matches(self):
        expr = StateOut('a', StateOut('b', StateMatch()))
        result = find2(expr, 'acbaaubbbbb', 0)
        assert list(result) == [(-1, -1)]

    def test_two_chars_one_match(self):
        expr = StateOut('a', StateOut('b', StateMatch()))
        result = find2(expr, 'ccvvvbbajbajbabb', 0)
        assert list(result) == [(14, 15)]

    def tests_find_two_chars_matches(self):
        expr = StateOut('a', StateOut('b', StateMatch()))
        result = find2(expr, 'baaaabbacaabbcc', 0)
        assert list(result) == [(5, 6), (11, 12)]

    def test_star_1(self):
        expr = StateSplit(None, StateMatch())
        expr.out = StateOut('c', expr)
        result = find2(expr, 'aaaabacccca', 0)
        assert list(result) == [(1, 0), (2, 1), (3, 2), (4, 3), (5, 4), (6, 5), (7, 10), (11, 10)]

    def test_star_2(self):
        expr = StateSplit(None, StateMatch())
        expr.out = StateOut('a', expr)
        result = find2(expr, 'aaaaaaaabacbca', 0)
        assert list(result) == [(1, 8), (9, 8), (10, 10), (11, 10), (12, 11), (13, 12), (14, 14)]

    def test_star_between_chars_star_match_end(self):
        star = StateSplit(None, StateMatch())
        star.out = StateOut('b', star)
        expr = StateOut('a', star)
        result = find2(expr, 'acjjjabcabbbbb', 0)
        assert list(result) == [(1, 1), (6, 7), (9, 14)]

    def test_star_and_char_star_not_match_end(self):
        star = StateSplit(None, StateMatch())
        star.out = StateOut('b', star)
        expr = StateOut('a', star)
        result = find2(expr, 'acjjjabcabbbbbfoobr', 0)
        assert list(result) == [(1, 1), (6, 7), (9, 14)]

    def test_star_between_chars_match_star(self):
        star = StateSplit(None, StateOut('c', StateMatch()))
        star.out = StateOut('b', star)
        expr = StateOut('a', star)
        result = find2(expr, 'xaabbbbbcjjjabcxalcac', 0)
        assert list(result) == [(3, 9), (13, 15), (20, 21)]






class TestPattern(object):
    def test_three_chars_no_matches(self):
        expr = Sequence(Sequence(Char('a'), Char('b')), Char('c'))
        result = find(expr, 'ccababababababacccbaccabbbc', 0)
        assert list(result) == [(-1, -1)]

    def test_three_chars_one_match(self):
        expr = Sequence(Sequence(Char('a'), Char('b')), Char('c'))
        result = find(expr, 'ccabababccbababacccbaccabbbc', 0)
        assert list(result) == [(7, 9)]

    def test_three_chars_one_matches_offset(self):
        expr = Sequence(Sequence(Char('a'), Char('b')), Char('c'))
        result = find(expr, 'abcjjjabc', 4)
        assert list(result) == [(7, 9)]

    def test_three_chars_negative_offset_no_match(self):
        expr = Sequence(Sequence(Char('a'), Char('b')), Char('c'))
        result = find(expr, 'abcjjjabc', -2)
        assert list(result) == [(-1, -1)]

    def test_three_chars_negative_offset_match(self):
        expr = Sequence(Sequence(Char('a'), Char('b')), Char('c'))
        result = find(expr, 'abcjjjabc', -3)
        assert list(result) == [(7, 9)]

    def test_three_chars_big_negative_offset_match(self):
        expr = Sequence(Sequence(Char('a'), Char('b')), Char('c'))
        result = find(expr, 'abcjjjabc', -100)
        assert list(result) == [(1, 3), (7, 9)]

    def test_three_chars_big_offset(self):
        expr = Sequence(Sequence(Char('a'), Char('b')), Char('c'))
        result = find(expr, 'abcjjjabc', 100)
        assert list(result) == [(-1, -1)]

    def test_star_1(self):
        expr = Star(Char('c'))
        result = find(expr, 'aaaabacccca', 0)
        assert list(result) == [(1, 0), (2, 1), (3, 2), (4, 3), (5, 4), (6, 5), (7, 10), (11, 10)]

    def test_star_2(self):
        expr = Star(Char('a'))
        result = find(expr, 'aaaaaaaabacbca', 0)
        assert list(result) == [(1, 8), (9, 8), (10, 10), (11, 10), (12, 11), (13, 12), (14, 14)]

    def test_star_between_chars_star(self):
        expr = Sequence(Char('a'), Star(Char('b')))
        result = find(expr, 'acjjjabc', 0)
        assert list(result) == (1, 1)

    def test_star_between_chars_match_star(self):
        expr = Sequence(Char('a'), Star(Char('b')))
        result = find(expr, 'xaabbbbbcjjjabc', 0)
        assert list(result) == [(2, 2), (3, 8), (13, 14)]

    def test_single_char_build_expr(self):
        expr = build_expr('a', False)
        assert expr.eq(Char('a'))

    def test_two_chars_build_expr(self):
        expr = build_expr('ab', False)
        assert expr.eq(Sequence(Char('a'), Char('b')))

    def test_three_chars_build_expr(self):
        expr = build_expr('abc', False)
        assert expr.eq(Sequence(Sequence(Char('a'), Char('b')), Char('c')))

    def test_chars_and_dots_build_expr(self):
        expr = build_expr('a.c.', False)
        assert expr.eq(
            Sequence(
                Sequence(
                    Sequence(Char('a'), Dot()),
                    Char('c')
                ),
                Dot()
            )
        )

    def test_chars_and_special_a_build_expr(self):
        expr = build_expr('%aa%a', False)
        assert expr.eq(
            Sequence(
                Sequence(CharRange(ord('A'), ord('z')), Char('a')),
                CharRange(ord('A'), ord('z'))
            )
        )

    def test_escape_percent_build_expr(self):
        expr = build_expr('%%', False)
        assert expr.eq(Char('%'))

    def test_build_expr_pattern_with_star(self):
        expr = build_expr('a*', False)
        assert expr.eq(Star(Char('a')))

    def test_build_expr_pattern_with_star_2(self):
        expr = build_expr('a*b*', False)
        assert expr.eq(
            Sequence(Star(Char('a')), Star(Char('b')))
        )

    def test_build_expr_pattern_with_star_3(self):
        expr = build_expr('a*cb*', False)
        assert expr.eq(
            Sequence(
                Sequence(Star(Char('a')), Char('c')),
                Star(Char('b'))
            )
        )

    def test_build_expr_pattern_with_star_4(self):
        expr = build_expr('a.*c%a*', False)
        assert expr.eq(
            Sequence(
                Sequence(
                    Sequence(Char('a'), Star(Dot())),
                    Char('c')
                ),
                Star(CharRange(ord('A'), ord('z')))
            )
        )
