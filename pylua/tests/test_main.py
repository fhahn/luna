from pylua.main import entry_point
from pylua.tests.fixtures import byte_file, uleb_file, luabytecode_file


def test_entry_point(luabytecode_file):
    entry_point([luabytecode_file])
