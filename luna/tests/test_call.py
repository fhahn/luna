import pytest

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

    def test_nested_function_tailcall(self):
        """
        Tests CALLMT with user defined function
        """
        ret = codetest("""
                function f(x)
                    y = x+1
                    return y
                end
                return f(f(5))
                """)
        assert ret.getval() == 7

    def test_nested_function_tailcall_builtin(self):
        """
        Tests CALLMT with builtin function
        """
        ret = codetest("""
                return math.sin(math.sin(1))
                """)
        assert ret.getval() == 0.7456241416655579

    def test_nested_function_call(self):
        """
        Tests CALLM with user function
        """
        ret = codetest("""
                function f(x)
                    y = x+1
                    return y
                end
                x = f(f(5))
                return x
                """)
        assert ret.getval() == 7

    def test_nested_function_call_builtin(self):
        """
        Tests CALLM with builtin function
        """
        ret = codetest("""
                x = math.sin(math.sin(1))
                return x
                """)
        assert ret.getval() == 0.7456241416655579

    def test_call_unknown_builtin(self):
        with pytest.raises(RuntimeError):
            codetest("""
                x = math.find(1)
            """)
