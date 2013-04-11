from .helpers import codetest


class TestInterpreter(object):

    def test_simple_add(self):
        """
        Tests addition with 16 bit number constants
        """
        ret = codetest("""
                x = 4
                y = 9
                z = x + y
                return x + y +z
                """)
        assert ret.returnvalue == 26

    def test_long_add(self):
        """
        Tests addition with number constants > 16 bit
        """
        ret = codetest("""
                x = 131072
                y = 131072
                z = x + y
                return z
                """)
        assert ret.returnvalue == 262144


