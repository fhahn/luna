import pytest

from luna.modules.patterns import (
    StateMatch, StateChar, find2, StateSplit, StateDot, StateCharRange,
    compile_re
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
        assert list(result) == [
            (1, 0), (2, 1), (3, 2), (4, 3), (5, 4), (6, 5), (7, 10),
            (11, 10)
        ]

    def test_star_2(self):
        expr = StateSplit(None, StateMatch())
        expr.out = StateChar('a', expr)
        result = find2(expr, 'aaaaaaaabacbca', 0)
        assert list(result) == [
            (1, 8), (9, 8), (10, 10), (11, 10), (12, 11), (13, 12), (14, 14)
        ]

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

    def test_simple_or(self):
        expr = compile_re('(aa|bb)')
        result = find2(expr, 'xyzabbaab', 0)
        assert list(result) == [(5, 6), (7, 8)]

    def test_grouped_or_between_chars(self):
        expr = compile_re('x(aa|bb)x')
        result = find2(expr, 'axaaxaxbxbbxa', 0)
        assert list(result) == [(2, 5), (9, 12)]

    def test_chained_grouped_or_match(self):
        expr = compile_re('x(aa|bb)(cc|dd)x')
        result = find2(expr, 'axaaddaxbbccxxaacx', 0)
        assert list(result) == [(8, 13)]

    def test_chained_grouped_or_no_match(self):
        expr = compile_re('x(aa|bb)(cc|dd)x')
        result = find2(expr, 'xaaccddxxaaddddxxaacc', 0)
        assert list(result) == [(-1, -1)]

    def test_grouped_star(self):
        expr = compile_re('(ab)*')
        result = find2(expr, 'ababababab', 0)
        assert list(result) == [(1, 10)]

    def test_grouped_star_between_chars_match(self):
        expr = compile_re('x(ab)*x')
        result = find2(expr, 'ababxababxabab', 0)
        assert list(result) == [(5, 10)]

    def test_grouped_star_between_chars_no_match(self):
        expr = compile_re('x(ab)*x')
        result = find2(expr, 'ababxabababab', 0)
        assert list(result) == [(-1, -1)]

    def test_grouped_star_and_or_match(self):
        expr = compile_re('x((aa)*|(bb)*)x')
        result = find2(expr, 'xaaaaaaxxx', 0)
        assert list(result) == [(1, 8), (9, 10)]

    def test_grouped_star_and_or_no_match(self):
        expr = compile_re('x((aa)*|(bb)*)x')
        result = find2(expr, 'xaaaaaxbxabxbbbb', 0)
        assert list(result) == [(-1, -1)]

    def test_or_repetition(self):
        expr = compile_re('(aa|bb){2}')
        result = find2(expr, 'xabbxaaaaxjkbbajbbaal', 0)
        assert list(result) == [(6, 9), (17, 20)]

    def test_single_char_build_expr(self):
        expr = compile_re('a')
        assert isinstance(expr, StateChar)
        assert expr.start == ord('a')
        assert expr.stop == ord('a')

    def test_two_chars_build_expr(self):
        expr = compile_re('ab')
        assert isinstance(expr, StateChar)
        assert expr.start == ord('a')
        assert isinstance(expr.out, StateChar)
        assert expr.out.start == ord('b')

    def test_three_chars_build_expr(self):
        expr = compile_re('abc')
        assert isinstance(expr, StateChar)
        assert expr.start == ord('a')
        assert isinstance(expr.out, StateChar)
        assert expr.out.start == ord('b')
        assert isinstance(expr.out.out, StateChar)
        assert expr.out.out.start == ord('c')

    def test_chars_and_dots_build_expr(self):
        expr = compile_re('a.c.', False)
        assert isinstance(expr, StateChar)
        assert expr.start == ord('a')
        assert isinstance(expr.out, StateDot)
        assert isinstance(expr.out.out, StateChar)
        assert expr.out.out.start == ord('c')
        assert isinstance(expr.out.out.out, StateDot)
        assert isinstance(expr.out.out.out.out, StateMatch)

    def test_chars_and_special_a_build_expr(self):
        expr = compile_re('%aa%a', False)
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
        expr = compile_re('%%', False)
        assert isinstance(expr, StateChar)
        assert expr.start == ord('%')
        assert isinstance(expr.out, StateMatch)

    def test_build_expr_pattern_with_star(self):
        expr = compile_re('a*', False)
        assert isinstance(expr, StateSplit)
        assert isinstance(expr.out, StateChar)
        assert expr.out.out == expr
        assert expr.out.start == ord('a')
        assert isinstance(expr.out2, StateMatch)

    def test_build_expr_pattern_with_star_2(self):
        expr = compile_re('a*b*', False)
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
        expr = compile_re('a*cb*', False)
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
        expr = compile_re('a.*c%a*', False)

        # a
        assert isinstance(expr, StateChar)
        assert expr.start == ord('a')

        # .*
        node = expr.out
        assert isinstance(node, StateSplit)
        assert isinstance(node.out, StateDot)
        assert node.out.out == node

        # c
        node = node.out2
        assert isinstance(node, StateChar)
        assert node.start == ord('c')

        # %a*
        node = node.out
        assert isinstance(node, StateSplit)
        assert isinstance(node.out, StateCharRange)
        assert node.out.start == ord('A')
        assert node.out.stop == ord('z')
        assert node.out.out == node

        # match
        node = node.out2
        assert isinstance(node, StateMatch)

    def test_build_expr_simple_or(self):
        expr = compile_re('a|b', False)

        # |
        assert isinstance(expr, StateSplit)

        # a
        node = expr.out
        assert isinstance(node, StateChar)
        assert node.stop == ord('a')
        assert isinstance(node.out, StateMatch)

        # b
        node = expr.out2
        assert isinstance(node, StateChar)
        assert node.stop == ord('b')
        assert isinstance(node.out, StateMatch)

    def test_build_group_star(self):
        expr = compile_re('(ab)*', False)

        # *
        assert isinstance(expr, StateSplit)

        # a
        node = expr.out
        assert isinstance(node, StateChar)
        assert node.stop == ord('a')

        # b
        node = node.out
        assert isinstance(node, StateChar)
        assert node.stop == ord('b')
        assert node.out == expr

        # match
        assert isinstance(expr.out2, StateMatch)

    def test_build_group_star_chained(self):
        expr = compile_re('(ab)*ab', False)

        # *
        assert isinstance(expr, StateSplit)

        # a
        node = expr.out
        assert isinstance(node, StateChar)
        assert node.stop == ord('a')

        # b
        node = node.out
        assert isinstance(node, StateChar)
        assert node.stop == ord('b')
        assert node.out == expr

        # ab
        node = expr.out2
        assert isinstance(node, StateChar)
        assert node.stop == ord('a')

        # b
        node = node.out
        assert isinstance(node, StateChar)
        assert node.stop == ord('b')

        # match
        assert isinstance(node.out, StateMatch)

    def test_build_group_or(self):
        expr = compile_re('(aa|bb)', False)

        # |
        assert isinstance(expr, StateSplit)

        # aa
        node = expr.out
        assert isinstance(node, StateChar)
        assert node.stop == ord('a')
        node = node.out
        assert isinstance(node, StateChar)
        assert node.stop == ord('a')
        assert isinstance(node.out, StateMatch)

        # bb
        node = expr.out2
        assert isinstance(node, StateChar)
        assert node.stop == ord('b')
        node = node.out
        assert isinstance(node, StateChar)
        assert node.stop == ord('b')
        assert isinstance(node.out, StateMatch)

    def test_build_group_or_between_chars(self):
        expr = compile_re('x(aa|bb)x')
        # xaax
        assert isinstance(expr, StateChar)
        assert expr.start == ord('x')

        # |
        node = expr.out
        assert isinstance(node, StateSplit)

        # aax
        node = node.out
        assert isinstance(node, StateChar)
        assert node.stop == ord('a')
        node = node.out
        assert isinstance(node, StateChar)
        assert node.stop == ord('a')
        node = node.out
        assert isinstance(node, StateChar)
        assert node.stop == ord('x')
        assert isinstance(node.out, StateMatch)

        # bbx
        node = expr.out.out2
        assert isinstance(node, StateChar)
        assert node.stop == ord('b')
        node = node.out
        assert isinstance(node, StateChar)
        assert node.stop == ord('b')
        node = node.out
        assert isinstance(node, StateChar)
        assert node.stop == ord('x')
        assert isinstance(node.out, StateMatch)

    def test_build_expr_with_repitition(self):
        expr = compile_re('a{3}')

        assert isinstance(expr, StateChar)
        assert isinstance(expr.out, StateChar)
        assert isinstance(expr.out.out, StateChar)
        assert isinstance(expr.out.out.out, StateMatch)


    def test_build_expr_misplaced_star(self):
        with pytest.raises(RuntimeError):
            compile_re('*')

    def test_build_expr_invalid_special_char(self):
        with pytest.raises(RuntimeError):
            compile_re('%,')

    def test_build_expr_misplaced_percent_1(self):
        with pytest.raises(RuntimeError):
            compile_re('%')

    def test_build_expr_misplaced_percent_2(self):
        with pytest.raises(RuntimeError):
            compile_re('a%%%')

    def test_build_expr_misplaced_percent_3(self):
        with pytest.raises(RuntimeError):
            compile_re('a%')


