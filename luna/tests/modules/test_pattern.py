from luna.modules.patterns import (
    StateMatch, StateChar, find2, StateSplit, StateDot, StateCharRange, build_expr
)


class TestPattern2(object):
    def test_single_char_no_match(self):
        expr = StateChar('c', StateMatch())
        result = find2(expr, 'xyz', 0)
        assert list(result) == [(-1, -1)]

    def test_single_char_one_match(self):
        expr = StateChar('c', StateMatch())
        result = find2(expr, 'asdasdxcz', 0)
        assert list(result) == [(8, 8)]

    def test_single_char_more_matches(self):
        expr = StateChar('c', StateMatch())
        result = find2(expr, 'xyzaaaccaa', 0)
        assert list(result) == [(7, 7), (8, 8)]

    def test_two_chars_no_matches(self):
        expr = StateChar('a', StateChar('b', StateMatch()))
        result = find2(expr, 'acbaaubbbbb', 0)
        assert list(result) == [(-1, -1)]

    def test_two_chars_one_match(self):
        expr = StateChar('a', StateChar('b', StateMatch()))
        result = find2(expr, 'ccvvvbbajbajbabb', 0)
        assert list(result) == [(14, 15)]

    def tests_find_two_chars_matches(self):
        expr = StateChar('a', StateChar('b', StateMatch()))
        result = find2(expr, 'baaaabbacaabbcc', 0)
        assert list(result) == [(5, 6), (11, 12)]

    def test_three_chars_no_matches(self):
        expr = StateChar('a', StateChar('b', StateChar('c', StateMatch())))
        result = find2(expr, 'ccababababababacccbaccabbbc', 0)
        assert list(result) == [(-1, -1)]

    def test_three_chars_one_match(self):
        expr = StateChar('a', StateChar('b', StateChar('c', StateMatch())))
        result = find2(expr, 'ccabababccbababacccbaccabbbc', 0)
        assert list(result) == [(7, 9)]

    def test_three_chars_two_matches(self):
        expr = StateChar('a', StateChar('b', StateChar('c', StateMatch())))
        result = find2(expr, 'babcccabababccbababacccbaccabbbc', 0)
        assert list(result) == [(2, 4), (11, 13)]

    def test_three_chars_one_matches_offset(self):
        expr = StateChar('a', StateChar('b', StateChar('c', StateMatch())))
        result = find2(expr, 'abcjjjabc', 4)
        assert list(result) == [(7, 9)]

    def test_three_chars_negative_offset_no_match(self):
        expr = StateChar('a', StateChar('b', StateChar('c', StateMatch())))
        result = find2(expr, 'abcjjjabc', -2)
        assert list(result) == [(-1, -1)]

    def test_three_chars_negative_offset_match(self):
        expr = StateChar('a', StateChar('b', StateChar('c', StateMatch())))
        result = find2(expr, 'abcjjjabc', -3)
        assert list(result) == [(7, 9)]

    def test_three_chars_big_negative_offset_match(self):
        expr = StateChar('a', StateChar('b', StateChar('c', StateMatch())))
        result = find2(expr, 'abcjjjabc', -100)
        assert list(result) == [(1, 3), (7, 9)]

    def test_three_chars_big_offset(self):
        expr = StateChar('a', StateChar('b', StateChar('c', StateMatch())))
        result = find2(expr, 'abcjjjabc', 100)
        assert list(result) == [(-1, -1)]

    def test_star_1(self):
        expr = StateSplit(None, StateMatch())
        expr.out = StateChar('c', expr)
        result = find2(expr, 'aaaabacccca', 0)
        assert list(result) == [(1, 0), (2, 1), (3, 2), (4, 3), (5, 4), (6, 5), (7, 10), (11, 10)]

    def test_star_2(self):
        expr = StateSplit(None, StateMatch())
        expr.out = StateChar('a', expr)
        result = find2(expr, 'aaaaaaaabacbca', 0)
        assert list(result) == [(1, 8), (9, 8), (10, 10), (11, 10), (12, 11), (13, 12), (14, 14)]

    def test_star_between_chars_star_match_end(self):
        star = StateSplit(None, StateMatch())
        star.out = StateChar('b', star)
        expr = StateChar('a', star)
        result = find2(expr, 'acjjjabcabbbbb', 0)
        assert list(result) == [(1, 1), (6, 7), (9, 14)]

    def test_star_and_char_star_not_match_end(self):
        star = StateSplit(None, StateMatch())
        star.out = StateChar('b', star)
        expr = StateChar('a', star)
        result = find2(expr, 'acjjjabcabbbbbfoobr', 0)
        assert list(result) == [(1, 1), (6, 7), (9, 14)]

    def test_star_between_chars_match_star(self):
        star = StateSplit(None, StateChar('c', StateMatch()))
        star.out = StateChar('b', star)
        expr = StateChar('a', star)
        result = find2(expr, 'xaabbbbbcjjjabcxalcac', 0)
        assert list(result) == [(3, 9), (13, 15), (20, 21)]

    def test_single_char_build_expr(self):
        expr = build_expr('a', False)
        assert isinstance(expr, StateChar)
        assert expr.start == ord('a')
        assert expr.stop == ord('a')

    def test_two_chars_build_expr(self):
        expr = build_expr('ab', False)
        assert isinstance(expr, StateChar)
        assert expr.start == ord('a')
        assert isinstance(expr.out, StateChar)
        assert expr.out.start == ord('b')

    def test_three_chars_build_expr(self):
        expr = build_expr('abc', False)
        assert isinstance(expr, StateChar)
        assert expr.start == ord('a')
        assert isinstance(expr.out, StateChar)
        assert expr.out.start == ord('b')
        assert isinstance(expr.out.out, StateChar)
        assert expr.out.out.start == ord('c')
 
    def test_chars_and_dots_build_expr(self):
        expr = build_expr('a.c.', False)
        assert isinstance(expr, StateChar)
        assert expr.start == ord('a')
        assert isinstance(expr.out, StateDot)
        assert isinstance(expr.out.out, StateChar)
        assert expr.out.out.start == ord('c')
        assert isinstance(expr.out.out.out, StateDot)
        assert isinstance(expr.out.out.out.out, StateMatch)

    def test_chars_and_special_a_build_expr(self):
        expr = build_expr('%aa%a', False)
        assert isinstance(expr, StateCharRange)
        assert expr.start == ord('A')
        assert expr.stop == ord('z')
        assert isinstance(expr.out, StateChar)
        assert expr.out.stop == ord('a')
        assert isinstance(expr.out.out, StateCharRange)
        assert expr.out.out.start == ord('A')
        assert expr.out.out.stop == ord('z')
        assert isinstance(expr.out.out.out, StateMatch)

    def test_escape_percent_build_expr(self):
        expr = build_expr('%%', False)
        assert isinstance(expr, StateChar)
        assert expr.start == ord('%')
        assert isinstance(expr.out, StateMatch)

    def test_build_expr_pattern_with_star(self):
        expr = build_expr('a*', False)
        assert isinstance(expr, StateSplit)
        assert isinstance(expr.out, StateChar)
        assert expr.out.out == expr
        assert expr.out.start == ord('a')
        assert isinstance(expr.out2, StateMatch)

    def test_build_expr_pattern_with_star_2(self):
        expr = build_expr('a*b*', False)
        assert isinstance(expr, StateSplit)
        assert isinstance(expr.out, StateChar)
        assert expr.out.out == expr
        assert expr.out.start == ord('a')
        assert isinstance(expr.out2, StateSplit)
        assert isinstance(expr.out2.out, StateChar)
        assert expr.out2.out.out == expr.out2
        assert expr.out2.out.start == ord('b')
        assert isinstance(expr.out2.out2, StateMatch)

    def test_build_expr_pattern_with_star_3(self):
        expr = build_expr('a*cb*', False)
        assert isinstance(expr, StateSplit)
        assert isinstance(expr.out, StateChar)
        assert expr.out.out == expr
        assert expr.out.start == ord('a')

        assert isinstance(expr.out2, StateChar)
        assert expr.out2.start == ord('c')

        assert isinstance(expr.out2.out, StateSplit)
        assert isinstance(expr.out2.out.out, StateChar)
        assert expr.out2.out.out.out == expr.out2.out
        assert expr.out2.out.out.start == ord('b')
        assert isinstance(expr.out2.out.out2, StateMatch)

    def test_build_expr_pattern_with_star_4(self):
        expr = build_expr('a.*c%a*', False)
        assert isinstance(expr, StateChar)
        assert expr.start == ord('a')

        assert isinstance(expr.out, StateSplit)
        # TODO Finish test case
