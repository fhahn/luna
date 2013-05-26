from .helpers import codetest


class TestWhile(object):
    """
    tests for the lua if then else and various comparisons
    """

    def test_simple_while(self):
        ret = codetest("""
                x = 0
                while x < 10 do
                    x = x + 1
                end
                return x
                """)
        assert ret.returnvalue == 10

    def test_simple_while_false(self):
        ret = codetest("""
                x = 99
                while x < 0 do
                    x = x + 1
                end
                return x
                """)
        assert ret.returnvalue == 99

    def test_complex_while(self):
        ret = codetest("""
                i = 0
                x = 0
                while i < 10 do
                    i = i + 1
                    x = x + 1
                    j = 5
                    while j > 0 do
                        j = j - 1
                        x = x + 1
                    end
                end
                return x
                """)
        assert ret.returnvalue == 60
