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
