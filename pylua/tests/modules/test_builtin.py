import pytest

from ..helpers import codetest, test_file


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

    def test_assert_with_stuff(self):
        codetest("""
                    assert(-2^- -2 == - - -4)
                """)

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

    def test_loadfile_simple(self):
        f = test_file(src='return "test"')
        ret = codetest("""
                    x = loadfile("%s")
                    return x()
                """ % f.name)
        assert ret.s_val == "test"

    def test_loadfile_function_with_params(self):
        f = test_file(src='''
                function foo(x, y)
                    return x + y
                end
                ''')
        ret = codetest("""
                    x = loadfile("%s")
                    x()
                    return foo(10, 20)
                """ % f.name)
        assert ret.n_val == 30

    def test_tonumber_int(self):
        ret = codetest("""
                    x = tonumber("100")
                    return x + 19
                """)
        assert ret.n_val == 119

    def test_tonumber_float(self):
        ret = codetest("""
                    x = tonumber("1.55")
                    return x + 19
                """)
        assert ret.n_val == 20.55

    def test_tonumber_invalid(self):
        ret = codetest("""
                    x = tonumber("str")
                    if x == nil then
                        return 10
                    else
                        return 99
                    end
                """)
        assert ret.n_val == 10

    def test_cat_strs(self):
        ret = codetest("""
                    return "hal".."lo"
                """)
        assert ret.s_val == "hallo"

    def test_cat_ints(self):
        ret = codetest("""
                    return 100 .. 99
                """)
        assert ret.s_val == "10099"

    def test_cat_str_int(self):
        ret = codetest("""
                    return "hallo" .. 99
                """)
        assert ret.s_val == "hallo99"

    def test_type_int(self):
        ret = codetest("""
                    x = 10
                    return type(x)
                """)
        assert ret.s_val == "number"

    def test_type_float(self):
        ret = codetest("""
                    x = 10.10
                    return type(x)
                """)
        assert ret.s_val == "number"

    def test_type_str(self):
        ret = codetest("""
                    x = "test"
                    return type(x)
                """)
        assert ret.s_val == "string"

    def test_type_table(self):
        ret = codetest("""
                    x = {1,2}
                    return type(x)
                """)
        assert ret.s_val == "table"

    def test_type_boolean(self):
        ret = codetest("""
                    x = false
                    return type(x)
                """)
        assert ret.s_val == "boolean"

    def test_type_mixed(self):
        ret = codetest("""
                    x = false
                    x = "string"
                    x = 10
                    x = "hallo"
                    return type(x)
                """)
        assert ret.s_val == "string"

