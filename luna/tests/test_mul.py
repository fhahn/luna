from .helpers import codetest


class TestMultiplication(object):
    def test_mulvn(self):
        ret = codetest("""
                x = 9
                return x * 4
                """)
        assert ret.getval() == 36

    def test_mulvn_long(self):
        ret = codetest("""
                x = 90000
                return x * 100000
                """)
        assert ret.getval() == 90000 * 100000

    def test_mulvn_float_int(self):
        ret = codetest("""
                x = 90000
                return x * 0.5
                """)
        assert ret.getval() == 45000

    def test_mulvn_int_float(self):
        ret = codetest("""
                x = 0.5
                return x * 90000
                """)
        assert ret.getval() == 45000

    def test_mulnv(self):
        ret = codetest("""
                x = 9
                return 4 * x
                """)
        assert ret.getval() == 36

    def test_mulnv_long(self):
        ret = codetest("""
                x = 90000
                return 100000 * x
                """)
        assert ret.getval() == 90000 * 100000

    def test_mulnv_float_int(self):
        ret = codetest("""
                x = 90000
                return 0.5 * x
                """)
        assert ret.getval() == 45000

    def test_mulnv_int_float(self):
        ret = codetest("""
                x = 0.5
                return 90000 * x
                """)
        assert ret.getval() == 45000

    def test_mulvv(self):
        ret = codetest("""
                x = 9
                y = 1000
                return x * y
                """)
        assert ret.getval() == 9000

    def test_mulvv_float_int(self):
        ret = codetest("""
                x = 0.5
                y = 1000
                return x * y
                """)
        assert ret.getval() == 500

    def test_mulvv_float_float(self):
        ret = codetest("""
                x = 0.5
                y = 0.25
                return x * y
                """)
        assert ret.getval() == 0.125

    def test_mulvv_long(self):
        ret = codetest("""
                x = 90000
                y = 100000
                return x * y
                """)
        assert ret.getval() == 90000 * 100000
