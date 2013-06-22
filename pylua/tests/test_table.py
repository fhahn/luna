from .helpers import codetest


class TestTable(object):
    def test_set_get_str_key_num(self):
        ret = codetest("""
                x = {}
                x["test"] = 99
                return x["test"]
                """)
        assert ret.getval() == 99

    def test_set_get_str_key_str(self):
        ret = codetest("""
                x = {}
                x["test"] = "str"
                return x["test"]
                """)
        assert ret.getval() == "str"

    def test_set_get_num_key_num(self):
        ret = codetest("""
                x = {}
                x[1] = 99
                return x[1]
                """)
        assert ret.getval() == 99

    def test_set_get_num_key_str(self):
        ret = codetest("""
                x = {}
                x[1] = "str"
                return x[1]
                """)
        assert ret.getval() == "str"

    def test_set_get_var_str_key_num(self):
        ret = codetest("""
                x = {}
                key = "key"
                x[key] = 99
                return x[key]
                """)
        assert ret.getval() == 99

    def test_set_get_var_str_key_str(self):
        ret = codetest("""
                x = {}
                key = "key"
                x[key] = "str"
                return x[key]
                """)
        assert ret.getval() == "str"

    def test_table_as_array_num(self):
        ret = codetest("""
                x = { 5, 2, 3}
                return x[1] + x[3]
                """)
        assert ret.getval() == 8

    def test_table_as_array_str(self):
        ret = codetest("""
                x = { "a", "b", "c"}
                return x[2]
                """)
        assert ret.getval() == "b"

    def test_table_constructor_str_vals(self):
        ret = codetest("""
                x =  {["foo"] = "bar", ["tmp"] = "dir"}
                return x["tmp"]
                """)
        assert ret.getval() == "dir"

    def test_table_constructor_num_vals(self):
        ret = codetest("""
                x =  {["foo"] = 100, ["tmp"] = 55}
                return x["tmp"] + x["foo"]
                """)
        assert ret.getval() == 100+55

    def test_table_constructor_num_key(self):
        ret = codetest("""
                x =  {["Foo"] = "bar", [111] = 1}
                return x[111]
                """)
        assert ret.getval() == 1

    def test_table_constructor_num_and_float_vals(self):
        ret = codetest("""
                x =  {["foo"] = 100.0001, ["tmp"] = 555.5}
                return x["tmp"] + x["foo"]
                """)
        assert ret.getval() == 100.0001+555.5

    def test_table_invalid_num_key(self):
        ret = codetest("""
                x =  {["foo"] = 100.0001, ["tmp"] = 555.5}
                return x[999]
        """)
        assert ret.getval() == 0

    def test_table_invalid_str_key(self):
        ret = codetest("""
                x =  {["foo"] = 100.0001, ["tmp"] = 555.5}
                return x["invlaid"]
        """)
        assert ret.getval() == 0

    def test_table_dot_key(self):
        ret = codetest("""
                x =  {["foo"] = 999}
                return x.foo
        """)
        assert ret.getval() == 999

    def test_table_same_int_and_str_as_key(self):
        ret = codetest("""
                x = {}
                x[111] = 99
                x["111"] = 10
                return x[111] + x["111"]
        """)
        assert ret.getval() == 99+10

    def test_table_concat(self):
        ret = codetest("""
                t = {"a", "b", "c"}
                return table.concat(t, ";")
        """)
        assert ret.getval() == "a;b;c"

    def test_table_concat_with_i_and_j(self):
        ret = codetest("""
                return table.concat({ 1, 2, "three", 4, "five" }, ", ", 2, 4)
        """)
        assert ret.getval() == "2, three, 4"

    def test_table_concat_with_i(self):
        ret = codetest("""
                return table.concat({ 1, 2, "three", 4, "five" }, ", ", 2)
        """)
        assert ret.getval() == "2, three, 4, five"

    def test_table_concat_no_sep(self):
        ret = codetest("""
                return table.concat({ 1, 2, "three", 4, "five" })
        """)
        assert ret.getval() == "12three4five"

    def test_table_insert_at_end(self):
        ret = codetest("""
                    t = {}
                table.insert(t, "c")
                table.insert(t, "b")
                table.insert(t, "a")
                return table.concat(t)
        """)
        assert ret.getval() == "cba"

    def test_table_insert_in_the_middle(self):
        ret = codetest("""
                t = {"d"}
                table.insert(t, 1, "c")
                table.insert(t, 1, "b")
                table.insert(t, 1, "a")
                return table.concat(t)
        """)
        assert ret.getval() == "abcd"
