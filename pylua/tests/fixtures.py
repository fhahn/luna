from subprocess import call

import pytest


def write_to_file(tmpdir, data):
    testfile = tmpdir.join('input.b')
    testfile.write(data, mode='wb')
    data = bytearray(data)
    return (testfile.dirname+'/'+testfile.basename, data)

@pytest.fixture
def byte_file(tmpdir):
    data = bytes("\xA0\x00\xBC\xFF\x98\x66\x66\xA0\x00\xBC\xFF\x98\x66\x66")
    return write_to_file(tmpdir, data)

@pytest.fixture
def uleb_file(tmpdir):
    return write_to_file(tmpdir, "\xE5\x8E\x26")

@pytest.fixture
def luabytecode_file(tmpdir):
    testfile = tmpdir.join('lua.l')
    testfile.write("x = 1")
    bc_file = testfile.dirname + '/out.b'
    call(['luajit', '-b', testfile.dirname+'/'+testfile.basename, bc_file])
    return bc_file