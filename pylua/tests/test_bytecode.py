from itertools import izip_longest
from subprocess import call

from pylua.bytecode import Parser
from pylua.tests.fixtures import byte_file, uleb_file, luabytecode_file



class TestParser:
    def test_byte(self, byte_file):
        p = Parser(byte_file[0])

        for b in byte_file[1]:
            assert p.byte() == b

    def test_word(self, byte_file):
        p = Parser(byte_file[0])

        def grouper(n, iterable, fillvalue=None):
            "Collect data into fixed-length chunks or blocks"
            # grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx
            args = [iter(iterable)] * n
            return izip_longest(fillvalue=fillvalue, *args)

        for w in grouper(4, byte_file[1]):
            # w can contain None, which breaks bytearray
            # remove None with generator
            assert p.word() == bytearray((i for i in w if i is not None))

    def test_uleb(self, uleb_file):
        p = Parser(uleb_file[0])
        assert p.uleb() == 624485

    def test_parse(self, luabytecode_file):
        """
        just checks if a valid bytecode file yields no exceptions
        """
        p = Parser(luabytecode_file)
        p.parse()

