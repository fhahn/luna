from ..helpers import codetest


class TestStringModule(object):
    def test_find_simple_pattern_match(self, capsys):
        codetest("""
            x, y = string.find('aabaajjbabaajaaaaa', 'aaa')
            print(x, y)
        """)
        out, _ = capsys.readouterr()
        assert out == "14 16\n"

    def test_find_simple_pattern_no_match(self, capsys):
        codetest("""
            x, y = string.find('aabaajjbabaajaaaaa', 'abc')
            print(x, y)
        """)
        out, _ = capsys.readouterr()
        assert out == "nil nil\n"

    def test_find_pattern_with_dot_match(self, capsys):
        codetest("""
            x, y = string.find('ajajajaccaabaa', '.b.')
            print(x, y)
        """)
        out, _ = capsys.readouterr()
        assert out == "11 13\n"

    def test_find_pattern_with_dot_no_match(self, capsys):
        codetest("""
            x, y = string.find('ajajajaccajyasda', '.b.')
            print(x, y)
        """)
        out, _ = capsys.readouterr()
        assert out == "nil nil\n"

    def test_find_simple_pattern_offset_match(self, capsys):
        codetest("""
            x, y = string.find("Hello Lua user", "Lua", 1)
            print(x, y)
        """)
        out, _ = capsys.readouterr()
        assert out == "7 9\n"

    def test_find_simple_pattern_offset_no_match(self, capsys):
        codetest("""
            x, y = string.find("Hello Lua user", "Lua", 8)
            print(x, y)
        """)
        out, _ = capsys.readouterr()
        assert out == "nil nil\n"

    def test_find_simple_pattern_negative_offset_match(self, capsys):
        codetest("""
            x, y = string.find("Hello Lua user", "e", -5)
            print(x, y)
        """)
        out, _ = capsys.readouterr()
        assert out == "13 13\n"

    def test_find_simple_pattern_big_negative_offset_match(self, capsys):
        codetest("""
            x, y = string.find("Hello Lua user", "e", -100)
            print(x, y)
        """)
        out, _ = capsys.readouterr()
        assert out == "2 2\n"

    def test_find_simple_pattern_big_offset_match(self, capsys):
        codetest("""
            x, y = string.find("Hello Lua user", "e", 100)
            print(x, y)
        """)
        out, _ = capsys.readouterr()
        assert out == "nil nil\n"

    def test_match_simple_pattern_no_match(self, capsys):
        codetest("""
            x = string.match('aabaajjbabaajaaaaa', 'abc')
            print(x)
        """)
        out, _ = capsys.readouterr()
        assert out == "nil\n"

    def test_match_simple_pattern_one_match(self, capsys):
        codetest("""
            x = string.match('aacbaajjbabaajaacabaabc', 'abc')
            print(x)
        """)
        out, _ = capsys.readouterr()
        assert out == "abc\n"

    def test_match_pattern_with_dot_no_match(self, capsys):
        codetest("""
            x = string.match('aaaajjbabaajaaaaa', '.b.c')
            print(x)
        """)
        out, _ = capsys.readouterr()
        assert out == "nil\n"

    def test_match_pattern_with_dot_match(self, capsys):
        codetest("""
            x = string.match('aaaajjbabaajaaxbycaa', '.b.c')
            print(x)
        """)
        out, _ = capsys.readouterr()
        assert out == "xbyc\n"
