import pytest

from .helpers import codetest


class TestStrings(object):
    def test_string_constant(self):
        ret = codetest("""
                    x = "str"
                    return x
                """)
        assert ret.s_val == "str"

    def test_empty_string_constant(self):
        ret = codetest("""
                    x = ""
                    return x
                """)
        assert ret.s_val == ""

    def test_cat_strs(self):
        ret = codetest("""
                    return "hal".."lo"
                """)
        assert ret.s_val == "hallo"

    def test_cat_ints(self):
        ret = codetest("""
                    return 100 .. 99
                """)
        assert ret.s_val == "10099"

    def test_cat_str_int(self):
        ret = codetest("""
                    return "hallo" .. 99
                """)
        assert ret.s_val == "hallo99"

    def test_cat_int_str_int(self):
        ret = codetest("""
                    return 1 .. ", " .. 99
                """)
        assert ret.s_val == "1, 99"
