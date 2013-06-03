from .helpers import codetest


class TestMultiplication(object):
    def test_mulvn(self):
        ret = codetest("""
                x = 9
                return x * 4
                """)
        assert ret.getval() == 36

    def test_mulnv(self):
        ret = codetest("""
                x = 9
                return 4 * x
                """)
        assert ret.getval() == 36

    def test_mulvv(self):
        ret = codetest("""
                x = 9
                y = 1000
                return x * y
                """)
        assert ret.getval() == 9000
