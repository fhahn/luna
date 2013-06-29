from .helpers import codetest


class TestReturn(object):
    """
    """
    def test_return_more_ints(self):
        ret = codetest("""
                function foo(i)
                    if i > 0 then
                        return i, foo(i-1)
                    else
                        return i, 0
                    end
                end
                x, y, z, a, b, c = foo(9)
                return x + y
                """)
        assert ret.getval() == 17
