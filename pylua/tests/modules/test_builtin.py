import pytest

from ..helpers import codetest


class TestBuiltin(object):
    def test_print_str(self, capsys):
        ret = codetest("""
                print("hallo")
                """)
        out, _ = capsys.readouterr()
        assert out == "hallo\n"

    def test_print_more_strings(self, capsys):
        ret = codetest("""
                print("hallo", "how", "are", "you")
                """)
        out, _ = capsys.readouterr()
        assert out == "hallo how are you\n"

    def test_print_int(self, capsys):
        ret = codetest("""
                print(1)
                """)
        out, _ = capsys.readouterr()
        assert out == "1\n"

    def test_print_int_var(self, capsys):
        ret = codetest("""
                x = 2
                print(x)
                """)
        out, _ = capsys.readouterr()
        assert out == "2\n"

    def test_print_more_ints(self, capsys):
        ret = codetest("""
                print(1, 2, 3)
                """)
        out, _ = capsys.readouterr()
        assert out == "1 2 3\n"

    def test_print_int_strings(self, capsys):
        ret = codetest("""
                print(2, "plus", 3, "=", 5)
                """)
        out, _ = capsys.readouterr()
        assert out == "2 plus 3 = 5\n"

    def test_print_int_strings_as_vars(self, capsys):
        ret = codetest("""
                x1 = 2
                x2 = "plus"
                x3 = 3
                x4 = "="
                x5 = 5
                print(x1, x2, x3, x4, x5)
                """)
        out, _ = capsys.readouterr()
        assert out == "2 plus 3 = 5\n"

    def test_assert_false_0(self):
        with pytest.raises(AssertionError) as ex:
            codetest("""
                        assert(0)
                    """)
        assert ex.exconly() == "AssertionError: assertion failed" 
    
    def test_assert_false_nil(self):
            with pytest.raises(AssertionError) as ex:
                codetest("""
                            assert(nil)
                        """)
            assert ex.exconly() == "AssertionError: assertion failed" 

    def test_assert_false_gt(self):
            with pytest.raises(AssertionError) as ex:
                codetest("""
                            assert(1 > 2)
                        """)
            assert ex.exconly() == "AssertionError: assertion failed" 

    def test_assert_false_with_vars_lt(self):
            with pytest.raises(AssertionError) as ex:
                codetest("""
                            x = 100
                            y = 10
                            assert(y > x)
                        """)
            assert ex.exconly() == "AssertionError: assertion failed" 

    def test_assert_false_with_msg(self):
            with pytest.raises(AssertionError) as ex:
                codetest("""
                            x = 100
                            y = 10
                            assert(y == x, "error")
                        """)
            assert ex.exconly() == "AssertionError: error" 

    def test_assert_false_with_and(self):
            with pytest.raises(AssertionError) as ex:
                codetest("""
                            assert(true and false)
                        """)

    def test_assert_true_with_or(self):
            with pytest.raises(AssertionError) as ex:
                codetest("""
                            assert(false or false)
                        """)

    def test_assert_true_1(self):
        codetest("""
                    assert(1)
                """)

    def test_assert_true_with_vars_lt(self):
            codetest("""
                        x = 100
                        y = 10
                        assert(y < x)
                    """)

    def test_assert_true_with_and(self):
            codetest("""
                        assert(true and true)
                    """)
    def test_assert_true_with_or(self):
            codetest("""
                        assert(false or true)
                    """)

