import sys

import pytest

from ..helpers import codetest, test_file
from luna.modules.patterns import match, Char, Sequence


class TestPattern(object):
    def test_single_char_no_match(self):
        expr = Char('c')
        matches = match(expr, 'xyz')
        assert matches == []

    def test_single_char_one_match(self):
        expr = Char('c')
        matches = match(expr, 'xcz')
        assert matches == [1]

    def test_single_char_more_matches(self):
        expr = Char('c')
        matches = match(expr, 'ccaaac')
        assert matches == [0, 1, 5]

    def test_two_chars_no_matches(self):
        expr = Sequence(Char('a'), Char('b'))
        matches = match(expr, 'acbaaubbbbb')
        assert matches == []

    def test_two_chars_one_match(self):
        expr = Sequence(Char('a'), Char('b'))
        matches = match(expr, 'ccabbbbbaaaaaa')
        assert matches == [2]

    def test_two_chars_two_matches(self):
        expr = Sequence(Char('a'), Char('b'))
        matches = match(expr, 'abbacaabbcc')
        assert matches == [0, 6]

    def test_three_chars_no_matches(self):
        expr = Sequence(Char('a'), Sequence(Char('b'), Char('c')))
        matches = match(expr, 'ccababababababacccbaccabbbc')
        assert matches == []
