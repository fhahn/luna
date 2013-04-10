from .helpers import codetest


class TestInterpreter(object):

    def test_simple_add(self):
        ret = codetest("""
                x = 4
                y = 9
                z = x + y
                return x + y +z
                """)
        assert ret.returnvalue == 26