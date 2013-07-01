from .helpers import codetest


class TestRepeat(object):
    """
    """
    def test_constant_return_0_args_1_ret(self):
        ret = codetest("""
                function foo()
                    return 2;
                end
                x = foo()
                return x
                """)
        assert ret.getval() == 2

    def test_call_1_arg_1_ret(self):
        ret = codetest("""
                function foo(x)
                    return x+1;
                end
                x = foo(10)
                return x
                """)
        assert ret.getval() == 11

    def test_call_2_args_1_ret(self):
        ret = codetest("""
                function foo(x, y)
                    return x+y;
                end
                x = foo(30, 10)
                return x
                """)
        assert ret.getval() == 40

    def test_call_2_args_ret_without_var(self):
        ret = codetest("""
                function foo(x, y)
                    return x+y;
                end
                return foo(30, 10)
                """)
        assert ret.getval() == 40

    def test_call_recursive(self):
        ret = codetest("""
                function fac(n)
                    if n == 1 then
                        return 1
                    end
                    x = n * fac(n-1);
                    print(n)
                    return x
                end
                x = fac(10)
                return x
                """)
        assert ret.getval() == 3628800
