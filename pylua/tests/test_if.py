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

    def test_iseqs_true_with_neq(self):
        ret = codetest("""
                x = "foo"
                if x ~= "bar" then
                    return 2
                end
                return 9
                """)
        assert ret.returnvalue == 2

    def test_iseqs_false_with_neq(self):
        ret = codetest("""
                x = "foo"
                if x ~= "foo" then
                    return 2
                end
                return 9
                """)
        assert ret.returnvalue == 9

    def test_isneqs_true_with_eq(self):
        ret = codetest("""
                x = "foo"
                if x == "foo" then
                    return 2
                end
                return 9
                """)
        assert ret.returnvalue == 2

    def test_isneqs_false_with_eq(self):
        ret = codetest("""
                x = "foo"
                if x == "bar" then
                    return 2
                end
                return 9
                """)
        assert ret.returnvalue == 9

    def test_iseqv_true_with_neq(self):
        ret = codetest("""
                x = "foo"
                y = "bar"
                if x ~= y then
                    return 2
                end
                return 9
                """)
        assert ret.returnvalue == 2

    def test_iseqv_false_with_neq(self):
        ret = codetest("""
                x = 101
                y = 101
                if x ~= y then
                    return 2
                end
                return 9
                """)
        assert ret.returnvalue == 9

    def test_isneqv_true_with_eq(self):
        ret = codetest("""
                x = "foo"
                y = "foo"
                if x == y then
                    return 2
                end
                return 9
                """)
        assert ret.returnvalue == 2

    def test_isneqv_false_with_eq(self):
        ret = codetest("""
                x = true
                y = false
                if x == y then
                    return 2
                end
                return 9
                """)
        assert ret.returnvalue == 9

    def test_isgt_true_with_str(self):
        ret = codetest("""
                x = "foo"
                y = "bar"
                if x >= y then
                    return 2
                end
                return 9
                """)
        assert ret.returnvalue == 2

    def test_isgt_false_with_str(self):
        ret = codetest("""
                x = "bar"
                y = "foo"
                if x >= y then
                    return 2
                end
                return 9
                """)
        assert ret.returnvalue == 9

    def test_isgt_true_with_num(self):
        ret = codetest("""
                x = 100
                y = 50
                if x >= y then
                    return 2
                end
                return 9
                """)
        assert ret.returnvalue == 2

    def test_isgt_false_with_num(self):
        ret = codetest("""
                x = 50
                y = 100
                if x >= y then
                    return 2
                end
                return 9
                """)
        assert ret.returnvalue == 9

    def test_isle_true_with_str(self):
        ret = codetest("""
                x = "foo"
                y = "bar"
                if not (x <= y) then
                    return 2
                end
                return 9
                """)
        assert ret.returnvalue == 2

    def test_isle_false_with_str(self):
        ret = codetest("""
                x = "bar"
                y = "foo"
                if not (x <= y) then
                    return 2
                end
                return 9
                """)
        assert ret.returnvalue == 9

    def test_isle_true_with_num(self):
        ret = codetest("""
                x = 100
                y = 50
                if not (x <= y) then
                    return 2
                end
                return 9
                """)
        assert ret.returnvalue == 2

    def test_isle_false_with_num(self):
        ret = codetest("""
                x = 50
                y = 100
                if not (x <= y) then
                    return 2
                end
                return 9
                """)
        assert ret.returnvalue == 9


