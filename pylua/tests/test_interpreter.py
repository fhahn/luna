from .helpers import codetest


class TestInterpreter(object):

    def test_short_add(self):
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
        used instructions: KNUM, GSET, GGET, ADDVV, RET1
        """
        ret = codetest("""
                x = 131072
                y = 131072
                z = x + y
                return z
                """)
        assert ret.returnvalue == 262144

    def test_add_constant_to_var(self):
        """
        Tests adding a constant to a variable,
        used instructions: KNUM, GSET, GGET, ADDVN, RET1
        """
        ret = codetest("""
                x = 131072
                return x+10
                """)
        assert ret.returnvalue == 131082

    def test_float_add(self):
        ret = codetest("""
                x = 6.5
                y = 1.2
                return x + y
                """)
        assert ret.returnvalue == 7.7
