import os
import subprocess

from luna.tests.helpers import test_file


class TestCompatibility(object):
    """
    Compatibility tests for Lua 5.1 from the
    official lua distribution
    """

    PYLUA_BIN = os.path.join(os.path.dirname(os.path.abspath(__file__)), ('../../bin/luna'))

    def test_constructs(self, capsys):
        test_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), ('scripts/constructs.lua'))
        out =  subprocess.check_output([TestCompatibility.PYLUA_BIN, test_file])
        assert out == "testing syntax\nOK\n"
