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
