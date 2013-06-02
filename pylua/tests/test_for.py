from .helpers import codetest


class TestFor(object):
    """
    """

    def test_simple_fori_loop(self):
        ret = codetest("""
                x = 0
                for i=1,10,1 do
                    x = x + 1
                end
                return x
                """)
        assert ret.getval() == 10

    def test_simple_fori_loop_false(self):
        ret = codetest("""
                x = 0
                for i=20,10,1 do
                    x = x + 1
                end
                return x
                """)
        assert ret.getval() == 0

    def test_simple_fori_loop_step_2(self):
        ret = codetest("""
                x = 0
                for i=1,10,2 do
                    x = x + 1
                end
                return x
                """)
        assert ret.getval() == 5

    def test_nested_fori_loop(self):
        ret = codetest("""
                x = 0
                for i=1,10,1 do
                    x = x + 1
                    for i=11,15,1 do
                        x = x + 2
                    end
                end
                return x
                """)
        assert ret.getval() == 110

    def test_backwards_fori_loop(self):
        ret = codetest("""
                x = 0
                for i=10,1,-1 do
                    x = x + 1
                end
                return x
                """)
        assert ret.getval() == 10

    def test_nested_backwards_fori_loop(self):
        ret = codetest("""
                x = 0
                for i=10,1,-1 do
                    x = x + 1
                    for i=11,15,1 do
                        x = x + 2
                    end
                end
                return x
                """)
        assert ret.getval() == 110
