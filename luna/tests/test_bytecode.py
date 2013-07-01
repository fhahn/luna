from luna.bytecode import Parser
from luna.tests.helpers import test_file, luabytecode_file


class TestParser:
    def test_byte(self):
        data = bytes("\xA0\x00\xBC\xFF\x98\x66\x66\xA0\x00\xBC\xFF\x98\x66\x66\x99\x80")
        f = test_file(data)

        p = Parser(f.name)
        for b in bytearray(data):
            assert p.byte() == b

    def test_word(self, ):
        data = bytes("\xA0\x00\xBC\xFF\x98\x66\x66\xA0\x00\xBC\xFF\x98\x66\x66\x99\x80")
        f = test_file(data)
        # little endian words (4 byte blocks)
        words = [0xffbc00a0,  0xa0666698, 0x98ffbc00, 0x80996666 ] 

        p = Parser(f.name)
        for w in words:
            x = p.word()
            print(hex(x))
            assert x == w

    def test_h(self):
        data = bytes("\xA0\x00\xBC\xFF\x98\x66\x66\xA0\x00\xBC\xFF\x98\x66\x66\x99\x80")
        f = test_file(data)
        # little endian 2 byte blocks
        bb = [0x00a0, 0xffbc, 0x6698, 0xa066, 0xbc00, 0x98ff, 0x6666, 0x8099]
        p = Parser(f.name)
        for h in bb:
            assert p.h() == h

    def test_uleb(self):
        f = test_file("\xE5\x8E\x26")
        p = Parser(f.name)
        assert p.uleb() == 624485

    def test_parse_simple_assignment(self):
        """
        checks if KSHORT, GSET and RET0 are decoded correctly
        """
        f = luabytecode_file("x = 1")
        p = Parser(f.name)
        flags, proto = p.parse()

        assert proto.constants[0].s_val == 'x'
        assert proto.instructions == [
            (39, (0, 1, 0)), (53, (0, 0, 0)), (71, (0, 1, 0))
        ]
