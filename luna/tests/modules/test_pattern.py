import sys

import pytest

from luna.modules.patterns import find, Char, Sequence, build_expr


class TestPattern(object):
    def test_single_char_no_match(self):
        expr = Char('c')
        result = find(expr, 'xyz')
        assert result == (-1, -1)

    def test_single_char_one_match(self):
        expr = Char('c')
        result = find(expr, 'asdasdxcz')
        assert result == (8, 8)

    def test_single_char_more_matches(self):
        expr = Char('c')
        result = find(expr, 'xyzaaaccaa')
        assert result == (7, 7)

    def test_two_chars_no_matches(self):
        expr = Sequence(Char('a'), Char('b'))
        result = find(expr, 'acbaaubbbbb')
        assert result == (-1, -1)

    def test_two_chars_one_match(self):
        expr = Sequence(Char('a'), Char('b'))
        result = find(expr, 'ccvvvbbajbajbabb')
        assert result == (14, 15)

    def test_two_chars_two_matches(self):
        expr = Sequence(Char('a'), Char('b'))
        result = find(expr, 'baaaabbacaabbcc')
        assert result == (5, 6)

    def test_three_chars_no_matches(self):
        expr = Sequence(Sequence(Char('a'), Char('b')), Char('c'))
        result = find(expr, 'ccababababababacccbaccabbbc')
        assert result == (-1, -1)

    def test_three_chars_one_matches(self):
        expr = Sequence(Sequence(Char('a'), Char('b')), Char('c'))
        result = find(expr, 'ccabababccbababacccbaccabbbc')
        assert result == (7, 9)

    def test_single_char_build_expr(self):
        expr = build_expr('a')
        assert isinstance(expr, Char)
        assert expr.c == 'a'

    def test_two_chars_build_expr(self):
        expr = build_expr('ab')
        assert isinstance(expr, Sequence)
        assert isinstance(expr.left, Char)
        assert isinstance(expr.right, Char)
        assert expr.left.c == 'a'
        assert expr.right.c == 'b'

    def test_three_chars_build_expr(self):
        expr = build_expr('abc')
        assert isinstance(expr, Sequence)
        assert isinstance(expr.left, Sequence)
        assert isinstance(expr.left.left, Char)
        assert isinstance(expr.left.right, Char)
        assert isinstance(expr.right, Char)
        assert expr.left.left.c == 'a'
        assert expr.left.right.c == 'b'
        assert expr.right.c == 'c'
