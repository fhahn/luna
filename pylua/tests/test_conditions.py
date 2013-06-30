from .helpers import codetest


class TestConditionals(object):
    """
    """

    def test_not_num1(self):
        ret = codetest("""
                return not 1
                """)
        assert ret.getval() == 1

    def test_not_num2(self):
        ret = codetest("""
                return not 2
                """)
        assert ret.getval() == 1

    def test_not_nil(self):
        ret = codetest("""
                return not nil
                """)
        assert ret.getval() == 2

    def test_not_false(self):
        ret = codetest("""
                return not false
                """)
        assert ret.getval() == 2

    def test_not_true(self):
        ret = codetest("""
                return not false
                """)
        assert ret.getval() == 2

    def test_not_string1(self):
        ret = codetest("""
                return not ""
                """)
        assert ret.getval() == 1

    def test_not_string2(self):
        ret = codetest("""
                return not "foo"
                """)
        assert ret.getval() == 1
