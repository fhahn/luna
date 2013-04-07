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

# always returns a bytearray
# TODO is there a better way to slice in rpython?
def slice(iterable, start, end):
    res = b'' 
    # TODO doesn't work with res as list, maybe a rpython bug?
    for i in xrange(start, min(end, len(iterable))):
        res += chr(iterable[i])
    return bytearray(res)

class Parser(object):
    def __init__(self, filename):
        f = os.open(filename, os.O_RDONLY, 0777)
        self.bytes = bytearray(os.read(f, 99999))
        self.pos = 0

    def next_bytes(self, l):
        v = slice(self.bytes, self.pos, self.pos+l)
        self.pos += l
        return v

    def byte(self):
        return self.next_bytes(1)[0]

    def word(self):
        return self.next_bytes(4)

    def uleb(self):
        #https://en.wikipedia.org/wiki/LEB128#Decode_unsigned_integer
        result = 0
        shift = 0
        while True:
            b = self.bytes[self.pos]
            self.pos += 1
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
            proto_buffer.append(self.next_bytes(l))
            if self.bytes[self.pos] == 0:
                break
        # 0U and EOF
        if self.uleb() != 0: raise ValueError("Missing 0U at end of file")
        print(self.pos, len(self.bytes))
        if self.pos < len(self.bytes): raise ValueError(" bytes leftover")

def entry_point(argv):
    try:
        filename = argv[1]
    except IndexError:
        print "You must supply a filename"
        return 1
    p = Parser(filename).parse()
    return 0

def target(*args):
    return entry_point, None

if __name__ == "__main__":
    entry_point(sys.argv)