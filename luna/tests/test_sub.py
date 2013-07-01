from .helpers import codetest


class TestSubtraction(object):
    def test_subvn(self):
        ret = codetest("""
                x = 6500
                return x - 3000
                """)
        assert ret.getval() == 3500

    def test_subvn_long(self):
        ret = codetest("""
                x = 113107200
                return x - 13107200
                """)
        assert ret.getval() == 100000000

    def test_subnv(self):
        ret = codetest("""
                x = 6500
                return 3000 - x
                """)
        assert ret.getval() == -3500

    def test_subnv_long(self):
        ret = codetest("""
                x = 13107200
                return 113107200 - x
                """)
        assert ret.getval() == 100000000

    def test_subvv(self):
        ret = codetest("""
                x = 6500
                y = 10000
                return y - x
                """)
        assert ret.getval() == 3500

    def test_subvv_long(self):
        ret = codetest("""
                x = 113107200
                y = 13107200
                return x - y
                """)
        assert ret.getval() == 100000000
