"""
    useful links:
        - http://wiki.luajit.org/Bytecode/c728f657001eaeee7f64eb99f47dc413c8e29a56
        - http://wiki.luajit.org/Bytecode-2.0
        - https://github.com/creationix/brozula/blob/master/parser.js
        - http://lua-users.org/lists/lua-l/2012-12/msg00229.html
        - http://luajit.org/running.html#opt_b

"""
import os
import struct

from rpython.annotator.model import SomeByteArray
from rpython.rlib.rstruct.runpack import runpack
from rpython.rlib.rstruct.ieee import float_unpack
from rpython.rlib.unroll import unrolling_iterable

from pylua.opcodes import OP_DESC, ARGS_AD, ARGS_ABC
from pylua.luaframe import LuaBytecodeFrame
from pylua.helpers import debug_print
from pylua.w_objects import W_Str, W_Num



KGC_TYPES = ["CHILD", "TAB", "I64", "U64", "COMPLEX", "STR", "const_str"]
UNROLLED_KGC_TYPES = unrolling_iterable(KGC_TYPES)

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
        self.frames = []
        while True:
            l = self.uleb()
            self.frames.append(self.parse_frame())
            # peek at next byte only, do not consume
            if self.peek() == 0:
                break
        # 0U and EOF
        if self.uleb() != 0: raise ValueError("Missing 0U at end of file")
        if self.pos < len(self.bytes): raise ValueError(" bytes leftover")
        return (flags, self.frames[-1])

    def parse_frame(self):
        flags = self.byte()
        num_params = self.byte()
        frame_size = self.byte()
        num_uv = self.byte()
        num_kgc = self.uleb()
        num_kn = self.uleb()
        num_bc = self.uleb()

        instructions = []
        debug_print("found "+ str(num_bc) + " bc instructions")
        for i in xrange(0, num_bc):
            instructions.append(self.decode_opcode(self.word()))

        debug_print("num uv "+str(num_uv))
        uv_data = []
        for i in xrange(0, num_uv):
            uv = self.h()
            uv_data.append((uv & 0x8000, uv & 0x4000, uv & 0x3fff))

        constants = [None] * (num_kgc+num_kn)

        childc = len(self.frames)
        #TODO imlement constant parsing
        for i in xrange(0, num_kgc):
            u = self.uleb()
            
            # CHILD 
            if u == 0:
                childc -= 1
                constants[num_kn+i] = self.frames[childc]
            else: # string and all other things
                constants[num_kn+i] = self.const_str(u)
            """
            for t in UNROLLED_KGC_TYPES:
                if t == kgc_type:
                    meth = getattr(self, t)
            """

        for i in xrange(0, num_kn):
            debug_print("read knum")
            constants[i] = self.read_knum()

        debug_print(str(constants))
        for (ind, args) in instructions:
            debug_print(str(OP_DESC[ind].name)+" "+str(args))

        return LuaBytecodeFrame(flags, constants, instructions)

    def const_str(self, l):
        l -= 5 # Offset for STR enum
        assert l > 0
        v = self.bytes[self.pos:self.pos+l]
        self.pos += l
        return W_Str(v)

    def read_knum(self):
        isnum = self.peek() & 1;
        lo = self.uleb() >> 1
        if isnum == 1:
            """
            IEEE 64 bit floating point constant
            """
            hi = self.uleb()
            hi = hi << 32
            res = float_unpack(lo | hi, 8)
            # TODO n_val can be a float or a int, can this lead
            # to problems when translating?
            return W_Num(res)
        return W_Num(lo)

    def decode_opcode(self, word):
        ind = word & 0xff
        op_desc = OP_DESC[ind]
        args_type = op_desc.args_type
        args = (0, 0, 0)
        a = (word >> 8) & 0xff
        if args_type == ARGS_AD:
            args =  (a, word >> 16, 0)
        elif args_type == ARGS_ABC:
            args = (a, word >> 24, (word >> 16) & 0xff)
        else:
            raise ValueError('Invalid argument type')
        return (ind, args)
