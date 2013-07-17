from luna.modules.patterns import (
    build_expr, find, Char, Sequence, Dot, CharRange, Star
)


class TestPattern(object):
    def test_single_char_no_match(self):
        expr = Char('c')
        result = find(expr, 'xyz', 0)
        assert result == (-1, -1)

    def test_single_char_one_match(self):
        expr = Char('c')
        result = find(expr, 'asdasdxcz', 0)
        assert result == (8, 8)

    def test_single_char_more_matches(self):
        expr = Char('c')
        result = find(expr, 'xyzaaaccaa', 0)
        assert result == (7, 7)

    def test_two_chars_no_matches(self):
        expr = Sequence(Char('a'), Char('b'))
        result = find(expr, 'acbaaubbbbb', 0)
        assert result == (-1, -1)

    def test_two_chars_one_match(self):
        expr = Sequence(Char('a'), Char('b'))
        result = find(expr, 'ccvvvbbajbajbabb', 0)
        assert result == (14, 15)

    def test_two_chars_two_matches(self):
        expr = Sequence(Char('a'), Char('b'))
        result = find(expr, 'baaaabbacaabbcc', 0)
        assert result == (5, 6)

    def test_three_chars_no_matches(self):
        expr = Sequence(Sequence(Char('a'), Char('b')), Char('c'))
        result = find(expr, 'ccababababababacccbaccabbbc', 0)
        assert result == (-1, -1)

    def test_three_chars_one_matches(self):
        expr = Sequence(Sequence(Char('a'), Char('b')), Char('c'))
        result = find(expr, 'ccabababccbababacccbaccabbbc', 0)
        assert result == (7, 9)

    def test_three_chars_one_matches_offset(self):
        expr = Sequence(Sequence(Char('a'), Char('b')), Char('c'))
        result = find(expr, 'abcjjjabc', 4)
        assert result == (7, 9)

    def test_three_chars_negative_offset_no_match(self):
        expr = Sequence(Sequence(Char('a'), Char('b')), Char('c'))
        result = find(expr, 'abcjjjabc', -2)
        assert result == (-1, -1)

    def test_three_chars_negative_offset_match(self):
        expr = Sequence(Sequence(Char('a'), Char('b')), Char('c'))
        result = find(expr, 'abcjjjabc', -3)
        assert result == (7, 9)

    def test_three_chars_big_negative_offset_match(self):
        expr = Sequence(Sequence(Char('a'), Char('b')), Char('c'))
        result = find(expr, 'abcjjjabc', -100)
        assert result == (1, 3)

    def test_three_chars_big_offset(self):
        expr = Sequence(Sequence(Char('a'), Char('b')), Char('c'))
        result = find(expr, 'abcjjjabc', 100)
        assert result == (-1, -1)

    def test_star_1(self):
        expr = Star(Char('c'))
        result = find(expr, 'aaaaaaaabacccca', 0)
        assert result == (1, 0)

    def test_star_2(self):
        expr = Star(Char('a'))
        result = find(expr, 'aaaaaaaabacccca', 0)
        assert result == (1, 8)

    def test_star_between_chars_star(self):
        expr = Sequence(Char('a'), Star(Char('b')))
        result = find(expr, 'acjjjabc', 0)
        assert result == (1, 1)

    def test_star_between_chars_match_star(self):
        expr = Sequence(Char('a'), Star(Char('b')))
        result = find(expr, 'xaaaabbbbbcjjjabc', 0)
        assert result == (2, 2)

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
