"""
    useful links:
        - http://wiki.luajit.org/Bytecode/c728f657001eaeee7f64eb99f47dc413c8e29a56
        - http://wiki.luajit.org/Bytecode-2.0
        - https://github.com/creationix/brozula/blob/master/parser.js
        - http://lua-users.org/lists/lua-l/2012-12/msg00229.html
        - http://luajit.org/running.html#opt_b

"""
import sys
import os
import struct
import array

from rpython.annotator.model import SomeByteArray
from rpython.rlib.rstruct.runpack import runpack

# always returns a bytearray
# TODO is there a better way to slice in rpython?
"""
def slice(iterable, start, end):
    res = b'' 
    # TODO doesn't work with res as list, maybe a rpython bug?
    for i in xrange(start, min(end, len(iterable))):
        res += chr(iterable[i])
    return bytearray(res)
"""
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

OP_DEF = {
    'KSHORT': {'A': 'dst', 'D': 'lits'},
    'GSET':   {'A': 'var', 'D': 'str'},
    'RET0':   {'A': 'rbase', 'D': 'lit'}
}

KGC_TYPES = ["CHILD", "TAB", "I64", "U64", "COMPLEX", "STR"]


class Arg(object):
    def __init__(self, val):
        self.val = val

class Proto(object):

    def __init__(self, p):
        self.flags = p.byte()
        self.num_params = p.byte()
        self.frame_size = p.byte()
        num_uv = p.byte()
        num_kgc = p.uleb()
        num_kn = p.uleb()
        num_bc = p.uleb()

        self.instructions = []
        print("found "+ str(num_bc) + " bc instructions")
        for i in xrange(0, num_bc):
            self.instructions.append(self.decode_opcode(p.word()))

        uv_data = []
        for i in xrange(0, num_uv):
            uv = p.h()
            uv_data.append((uv & 0x8000, uv & 0x4000, uv & 0x3fff))

        self.constants = []

        #TODO imlement constant parsing
        for i in xrange(0, num_kgc):
            # STR constant parsing
            c_type = "STR"
            l = kgc_type = p.uleb()
            l -= 5 # Offset for STR enum
            assert l > 0
            self.constants.append(p.bytes[p.pos:p.pos+l])
            p.pos += l
        self.num_consts = len(self.constants)
        print(self.constants, self.instructions)

    def decode_opcode(self, word):
        ind = word & 0xff
        code = OPCODES[ind]
        op_def = OP_DEF[code]
        args = []

        # A
        args.append((word >> 8) & 0xff)

        # D
        if 'D' in op_def:
            args.append(word >> 16)
        else:
            args.append((word >> 16) & 0xff)
            args.append(word >> 24)

        return (code, args)


    """
    def decode_arg(self, type, val):
        if type == 'lit':  # literal
            return Arg(val >> 0)#?
        elif type == 'lits': # signed literal
            return Arg(0x10000 - val if (val & 0x8000) > 0 else val)
        elif type == 'pri':
            if val == 0: return Arg(None)
            elif val == 1: return Arg(False)
            elif val == 2: return Arg(True)
            else: assert 0 
        elif type == 'num': return Arg(val) #return self.constants[val]
        elif type in ('str', 'tab', 'func', 'cdata'):
            return Arg(self.constants[self.num_consts-val-1])
        elif type == 'jump':
            return Arg(val - 0x8000)
        else:
         return Arg(val)
    """



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
        protos = []
        while True:
            l = self.uleb()
            protos.append(Proto(self))
            # peek at next byte only, do not consume
            if self.peek() == 0:
                break
        # 0U and EOF
        if self.uleb() != 0: raise ValueError("Missing 0U at end of file")
        if self.pos < len(self.bytes): raise ValueError(" bytes leftover")
        return (flags, protos)
