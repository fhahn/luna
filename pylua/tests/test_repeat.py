from .helpers import codetest


class TestRepeat(object):
    """
    tests for the lua if then else and various comparisons
    """

    def test_simple_repeat(self):
        ret = codetest("""
                x = 0
                repeat
                    x = x + 1
                until x == 10
                return x
                """)
        assert ret.returnvalue == 10

    def test_simple_repeat_false(self):
        ret = codetest("""
                x = 99
                repeat
                    x = x + 1
                until x > 0
                return x
                """)
        assert ret.returnvalue == 100

    def test_nested_repeat(self):
        ret = codetest("""
                i = 0
                x = 0
                repeat
                    i = i + 1
                    x = x + 1
                    j = 5
                    repeat
                        j = j - 1
                        x = x + 1
                    until j == 0
                until i == 10
                return x
                """)
        assert ret.returnvalue == 60
