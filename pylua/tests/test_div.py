from .helpers import codetest


class TestDivision(object):
    def test_divvn(self):
        ret = codetest("""
                x = 4
                return x / 2
                """)
        assert ret.getval() == 2

    def test_divnv(self):
        ret = codetest("""
                x = 4
                return 16 / x
                """)
        assert ret.getval() == 4

    def test_divvv(self):
        ret = codetest("""
                x = 10000
                y = 1000
                return x / y
                """)
        assert ret.getval() == 10

    def test_divvn_float(self):
        ret = codetest("""
                x = 5.0
                return x / 2.0
                """)
        assert ret.getval() == 2.5

    def test_divnv_float(self):
        ret = codetest("""
                x = 2
                return 35 / x
                """)
        assert ret.getval() == 17.5

    def test_divvv_float(self):
        ret = codetest("""
                x = 2.5
                y = 2
                return x / y
                """)
        assert ret.getval() == 1.25
