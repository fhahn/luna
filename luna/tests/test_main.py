import os

from luna.main import main
from luna.tests.helpers import luabytecode_file, test_file


class TestMain(object):
    def test_with_bytecode_file(self):
        f = luabytecode_file("x = 1")
        assert main(['', f.name]) == 0

    def test_with_lua_file(self):
        f = test_file("x = 1", suffix=".l")
        assert main(['', f.name]) == 0
        assert os.path.exists(f.name+'c')

    def test_with_non_exisiting_file(self, tmpdir):
        assert main(['', tmpdir.dirname+'/'+'foo.l']) == 1

    def test_with_invalid_extension(self):
        f = test_file("int main(void{};", suffix=".c")
        assert main(['', f.name]) == 1

    def test_with_invalid_lua_file(self):
        f = test_file("this is no lua code", suffix=".l")
        assert main(['', f.name]) == 1
