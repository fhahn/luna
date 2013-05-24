from .helpers import codetest


class TestIf(object):
    """
    tests for the lua if then else and various comparisons
    """

    def test_isnen_false_with_eq(self):
        ret = codetest("""
                x = 99
                if x == 99 then
                    return 2
                end
                return 9
                """)
        assert ret.returnvalue == 2

    def test_isnen_true_with_eq(self):
        ret = codetest("""
                x = 99;
                if x == 88 then
                    return 2;
                end
                return 9;
                """)
        assert ret.returnvalue == 9

    def test_iseqn_false_with_neq(self):
        ret = codetest("""
                x = 99
                if x ~= 99 then
                    return 2
                end
                return 9
                """)
        assert ret.returnvalue == 9

    def test_iseqn_true_with_neq(self):
        ret = codetest("""
                x = 99
                if x ~= 88 then
                    return 2
                end
                return 9
                """)
        assert ret.returnvalue == 2

    def test_iseqp_true_with_neq(self):
        ret = codetest("""
                x = true
                if x ~= false then
                    return 2
                end
                return 9
                """)
        assert ret.returnvalue == 2

    def test_iseqp_false_with_neq(self):
        ret = codetest("""
                x = false
                if x ~= false then
                    return 2
                end
                return 9
                """)
        assert ret.returnvalue == 9

    def test_isneqp_true_with_eq(self):
        ret = codetest("""
                x = true
                if x == true then
                    return 2
                end
                return 9
                """)
        assert ret.returnvalue == 2

    def test_isneqp_false_with_eq(self):
        ret = codetest("""
                x = false
                if x == true then
                    return 2
                end
                return 9
                """)
        assert ret.returnvalue == 9
