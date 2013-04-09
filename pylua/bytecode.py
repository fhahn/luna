"""
    useful links:
        - http://wiki.luajit.org/Bytecode/c728f657001eaeee7f64eb99f47dc413c8e29a56
        - http://wiki.luajit.org/Bytecode-2.0
        - https://github.com/creationix/brozula/blob/master/parser.js
        - http://lua-users.org/lists/lua-l/2012-12/msg00229.html
        - http://luajit.org/running.html#opt_b

"""
import os

from rpython.annotator.model import SomeByteArray
from rpython.rlib.rstruct.runpack import runpack

OPCODES = [
  "ISLT", "ISGE", "ISLE", "ISGT", "ISEQV", "ISNEV", "ISEQS", "ISNES", "ISEQN",
  "ISNEN", "ISEQP", "ISNEP", "ISTC", "ISFC", "IST", "ISF", "MOV", "NOT", "UNM",
  "LEN", "ADDVN", "SUBVN", "MULVN", "DIVVN", "MODVN", "ADDNV", "SUBNV", "MULNV",
  "DIVNV", "MODNV", "ADDVV", "SUBVV", "MULVV", "DIVVV", "MODVV", "POW", "CAT",
  "KSTR", "KCDATA", "KSHORT", "KNUM", "KPRI", "KNIL", "UGET", "USETV", "USETS",
  "USETN", "USETP", "UCLO", "FNEW", "TNEW", "TDUP", "GGET", "GSET", "TGETV",
  "TGETS", "TGETB", "TSETV", "TSETS", "TSETB", "TSETM", "CALLM", "CALL",
  "CALLMT", "CALLT", "ITERC", "ITERN", "VARG", "ISNEXT", "RETM", "RET", "RET0",
  "RET1", "FORI", "JFORI", "FORL", "IFORL", "JFORL", "ITERL", "IITERL",
  "JITERL", "LOOP", "ILOOP", "JLOOP", "JMP", "FUNCF", "IFUNCF", "JFUNCF",
  "FUNCV", "IFUNCV", "JFUNCV", "FUNCC", "FUNCCW"
]

class Proto(object):

    def __init__(self, p):
        self.flags = p.byte()
        self.num_params = p.byte()
        self.frame_size = p.byte()
        self.num_uv = p.byte()
        self.num_kgc = p.uleb()
        self.num_kn = p.uleb()
        self.num_bc = p.uleb()

        bc_ins = []
        print("found "+ str(self.num_bc) + " bc instructions")
        print self.flags, self.num_params, self.frame_size, self.num_uv, self.num_kgc, self.num_kn, self.num_bc
        for i in xrange(0, self.num_bc):
            self.decode_opcode(p.word())

        uv_data = []
        for i in xrange(0, self.num_uv):
            uv = p.h()
            uv_data.append((uv & 0x8000, uv & 0x4000, uv & 0x3fff))

        constants = []
        #TODO imlement constant parsing
        for i in xrange(0, self.num_kgc):
            constants.append(p.uleb())

        # TODO parse constants
        for i in xrange(0, self.num_kgc):
            constants.append(p.uleb())
    def decode_opcode(self, word):
        ind = word & 0xff
        code = OPCODES[ind]
        print ind, code, word


class Parser(object):
    def __init__(self,  filename):
        if isinstance(filename, SomeByteArray):
            self.bytes = filename
        else:
            f = os.open(filename, os.O_RDONLY, 0777)
            self.bytes = bytes(os.read(f, 99999))
        self.pos = 0

    def next_bytes(self, l):
        if self.pos >= 0:
            v = self.bytes[self.pos:self.pos+l]
            self.pos += l
            return v

    def byte(self):
        return runpack('=B', self.next_bytes(1))

    def peek(self):
        return runpack('=B', self.bytes[self.pos])

    def h(self):
        return runpack('=H', self.next_bytes(2))

    def word(self):
        return runpack('=I', self.next_bytes(4))

    def uleb(self):
        #https://en.wikipedia.org/wiki/LEB128#Decode_unsigned_integer
        result = 0
        shift = 0
        while True:
            b = self.byte()
            result |= (b & 0x7f) << shift
            if b & 0x80 == 0:
                break
            shift += 7
        return result

    def parse(self):
        # parses a luajit bytecode file 
        # see http://wiki.luajit.org/Bytecode-2.0 for format information

        # header = ESC 'L' 'J' versionB flagsU [namelenU nameB*]
        if self.byte() != 0x1b: raise ValueError("Expected ESC in first byte")
        if self.byte() != 0x4c: raise ValueError("Expected L in second byte")
        if self.byte() != 0x4a: raise ValueError("Expected J in third byte")
        if self.byte() != 1: raise ValueError("Only version 1 supported")

        # flags
        flags = self.uleb()

        # proto+    
        proto_buffer = []
        while True:
            l = self.uleb()
            print self.pos, len(self.bytes),l 
            Proto(self)
            # peek at next byte only, do not consume
            if self.peek() == 0:
                break
        # 0U and EOF
        if self.uleb() != 0: raise ValueError("Missing 0U at end of file")
        if self.pos < len(self.bytes): raise ValueError(" bytes leftover")
