import os
import subprocess

from pylua.tests.helpers import test_file


class TestCompiled(object):
    """
    Tests compiled binary
    """

    PYLUA_BIN = os.path.join(os.path.dirname(os.path.abspath(__file__)), ('../../bin/pylua'))

    def test_addition(self, capsys):
        f = test_file(src="""
            -- short add
            x = 10
            y = 5
            z = y + y + x
            print(z)
            print(z+y)
            --a = 100+y

            lx = 1234567890.55
            ly = 99999999
            print(lx+ly)
            --print(lx+1234567890)
            """, suffix=".l"
        )
        out =  subprocess.check_output([TestCompiled.PYLUA_BIN, f.name])
        assert out == "20\n25\n1334567889.550000\n"

    def test_if_with_num(self, capsys):
        f = test_file(src="""
            x = 10
            y = 5
            if x == 10 then
                print ("OK1")
            end
            
            if x ~= 10 then
                print ("F1")
            end

            if x < y then
                print ("F2")
            end

            if x <= y then
                print ("F3")
            end

            if x > y then
                print ("OK2")
            end

            if x >= y then
                print ("OK3")
            end

            if x == y then
                print ("F4")
            end

             if x ~= y then
                print ("OK4")
            end

            xx = 10

            if x == xx then
                print ("OK5")
            end

            if x >= xx then
                print ("OK6")
            end

            if x <= xx then
                print ("OK7")
            end
            """, suffix=".l"
        )
        out =  subprocess.check_output([TestCompiled.PYLUA_BIN, f.name])
        assert out == "OK1\nOK2\nOK3\nOK4\nOK5\nOK6\nOK7\n"

    def test_if_with_str(self, capsys):
        f = test_file(src="""
            x = "foo"
            y = "bar"
            if x == "foo" then
                print ("OK1")
            end

            if x ~= "foo" then
                print ("F1")
            end

            if x < y then
                print ("F2")
            end

            if x <= y then
                print ("F3")
            end

            if x > y then
                print ("OK2")
            end

            if x >= y then
                print ("OK3")
            end

            if x == y then
                print ("F4")
            end

             if x ~= y then
                print ("OK4")
            end

            xx = "foo"

            if x == xx then
                print ("OK5")
            end

            if x >= xx then
                print ("OK6")
            end

            if x <= xx then
                print ("OK7")
            end
            """, suffix=".l"
        )
        out =  subprocess.check_output([TestCompiled.PYLUA_BIN, f.name])
        assert out == "OK1\nOK2\nOK3\nOK4\nOK5\nOK6\nOK7\n"

    def test_if_with_bool(self, capsys):
        f = test_file(src="""
            x = true
            y = false
            if x == true then
                print ("OK1")
            end

            if x ~= true then
                print ("F1")
            end

            if x == y then
                print("F2")
            end

            if x ~= y then
                print("OK2")
            end

            if true == x then
                print ("OK3")
            end

            if y == true then
                print("F3")
            end
            """, suffix=".l"
        )
        out =  subprocess.check_output([TestCompiled.PYLUA_BIN, f.name])
        assert out == "OK1\nOK2\nOK3\n"

    def test_recursive_call(self):

        f = test_file(src="""
            function fac(n)
                if n == 1 then
                    return 1
                end
                return fac(n-1) * n
            end
            x = fac(10)
            print(x)
            """, suffix=".l"
        )
        out =  subprocess.check_output([TestCompiled.PYLUA_BIN, f.name])
        assert out == "3628800\n"
