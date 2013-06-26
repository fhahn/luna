from .helpers import codetest


class TestReturn(object):
    """
    """
    def test_return_more_ints(self):
        ret = codetest("""
                function foo()
                    return 1, 2, 3
                end
                x, y, z = foo()
                return x + y + z
                """)
        assert ret.getval() == 6
