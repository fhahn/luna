import os
import subprocess

from pylua.tests.helpers import test_file


class TestCompiled(object):
    """
    Tests compiled binary
    """

    def test_addition(self, capsys):
        f = test_file(src="""
            -- short add
            x = 10
            y = 5
            z = y + y + x
            print(z)
            print(z+y)
            --a = 100+y

            lx = 1234567890
            ly = 99999999
            print(lx+ly)
            --print(lx+1234567890)
            """, suffix=".l"
        )
        out =  subprocess.check_output(['bin/pylua', f.name])
        assert out == "20.000000\n25.000000\n1334567889.000000\n"
