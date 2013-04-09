from subprocess import call

import pytest


def write_to_file(tmpdir, data):
    testfile = tmpdir.join('input.b')
    testfile.write(data, mode='wb')
    data = bytearray(data)
    return (testfile.dirname+'/'+testfile.basename, data)

@pytest.fixture
def byte_file(tmpdir):
    data = bytes("\xA0\x00\xBC\xFF\x98\x66\x66\xA0\x00\xBC\xFF\x98\x66\x66\x99\x80")
    res = write_to_file(tmpdir, data)
    return {'path': res[0], 'bytes': res[1], 
            '2bytes': [0x00a0, 0xffbc, 0x6698, 0xa066, 0xbc00, 0x98ff, 0x6666, 0x8099],
            'words': [0xffbc00a0,  0xa0666698, 0x98ffbc00, 0x80996666 ]
            }  

@pytest.fixture
def uleb_file(tmpdir):
    return write_to_file(tmpdir, "\xE5\x8E\x26")

@pytest.fixture
def luabytecode_file(tmpdir):
    testfile = tmpdir.join('lua.l')
    testfile.write("x = 1")
    bc_file = testfile.dirname + '/out.lc'
    call(['luajit', '-b', testfile.dirname+'/'+testfile.basename, bc_file])
    return bc_file

@pytest.fixture
def luacode_file(tmpdir):
    testfile = tmpdir.join('lua.l')
    testfile.write("x = 1")
    path = testfile.dirname + '/' + testfile.basename
    return path