import sys

import pytest

from ..helpers import codetest, test_file


class TestMath(object):
    def test_huge(self, capsys):
        ret = codetest("""
                return math.huge
                """)
        assert ret.n_val == sys.maxint

    def test_floor_1(self, capsys):
        ret = codetest("""
                return math.floor(1.9)
                """)
        assert ret.n_val == 1

    def test_floor_2(self, capsys):
        ret = codetest("""
                return math.floor(1.0)
                """)
        assert ret.n_val == 1

    def test_floor_3(self, capsys):
        ret = codetest("""
                return math.floor(-1.1)
                """)
        assert ret.n_val == -2 