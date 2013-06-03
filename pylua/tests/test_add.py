from .helpers import codetest


class TestAddition(object):
    def test_addvv(self):
        ret = codetest("""
                x = 4
                y = 9
                z = x + y
                return x + y +z
                """)
        assert ret.getval() == 26

    def test_addvv_long(self):
        ret = codetest("""
                x = 131072
                y = 131072
                z = x + y
                return z
                """)
        assert ret.getval() == 262144

    def test_addvv_float(self):
        ret = codetest("""
                x = 6.5
                y = 1.2
                return x + y
                """)
        assert ret.getval() == 7.7

    def test_addvn(self):
        ret = codetest("""
                x = 131072
                return x+10
                """)
        assert ret.getval() == 131082

    def test_addnv(self):
        ret = codetest("""
                x = 131
                return 10 + x
                """)
        assert ret.getval() == 141
