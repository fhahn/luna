from itertools import izip_longest

from pylua.bytecode import Parser
from pylua.tests.fixtures import byte_file, uleb_file, luabytecode_file

from pylua.instructions import *


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

    def test_parse_simple_assignment(self, luabytecode_file):
        """
        checks if KSHORT, GSET and RET0 are decoded correctly
        """
        p = Parser(luabytecode_file)
        flags, protos = p.parse()
        proto = protos[0]

        assert proto.constants == ['x']

        assert isinstance(proto.instructions[0], KSHORT)
        assert proto.instructions[0].a == 0
        assert proto.instructions[0].d == 1

        assert isinstance(proto.instructions[1], GSET)
        assert proto.instructions[1].a == 0
        assert proto.instructions[1].d == 0

        assert isinstance(proto.instructions[2], RET0)
        assert proto.instructions[2].a == 0
        assert proto.instructions[2].d == 1
   
