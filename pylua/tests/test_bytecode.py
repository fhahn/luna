from itertools import izip_longest

from pylua.bytecode import Parser
from pylua.tests.fixtures import byte_file, uleb_file, luabytecode_file



class TestParser:
    def test_byte(self, byte_file):
        p = Parser(byte_file['path'])

        for b in byte_file['bytes']:
            assert p.byte() == b

    def test_word(self, byte_file):
        p = Parser(byte_file['path'])
        for w in byte_file['words']:
            # w can contain None, which breaks bytearray
            # remove None with generator
            assert p.word() == w

    def test_h(self, byte_file):
        p = Parser(byte_file['path'])
        for h in byte_file['2bytes']:
            # w can contain None, which breaks bytearray
            # remove None with generator
            assert p.h() == h

    def test_uleb(self, uleb_file):
        p = Parser(uleb_file[0])
        assert p.uleb() == 624485

    def test_parse(self, luabytecode_file):
        """
        just checks if a valid bytecode file yields no exceptions
        """
        p = Parser(luabytecode_file)
        p.parse()
