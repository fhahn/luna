from .helpers import codetest


class TestIf(object):

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


