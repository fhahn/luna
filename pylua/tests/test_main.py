import os

from pylua.main import main
from pylua.tests.fixtures import luabytecode_file, luacode_file


class TestMain(object):
    def test_with_bytecode_file(self, luabytecode_file):
        print luabytecode_file
        assert main(['', luabytecode_file]) == 0

    def test_with_lua_file(self, luacode_file):
        assert main(['', luacode_file]) == 0
        assert os.path.exists(luacode_file+'c')

    def test_with_non_exisiting_file(self, tmpdir):
        assert main(['', tmpdir.dirname+'/'+'foo.l']) == 1

    def test_with_invalid_extension(self, tmpdir):
        f = tmpdir.join('test.c')
        assert main(['', f.dirname+'/'+f.basename]) == 1

    def test_with_invalid_lua_file(self, tmpdir):
        f = tmpdir.join('test.l')
        f.write('this is no lua code')
        assert main(['', f.dirname+'/'+f.basename]) == 1
