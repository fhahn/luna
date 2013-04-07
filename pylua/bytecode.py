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
        v = self.bytes[self.pos]
        self.pos += 1
        return v

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

def parse(filename):
    # parses a luajit bytecode file 
    # see http://wiki.luajit.org/Bytecode-2.0 for format information
    parser = Parser(filename)

    # header = ESC 'L' 'J' versionB flagsU [namelenU nameB*]
    if parser.byte() != 0x1b: raise ValueError("Expected ESC in first byte");
    if parser.byte() != 0x4c: raise ValueError("Expected L in second byte");
    if parser.byte() != 0x4a: raise ValueError("Expected J in third byte");
    if parser.byte() != 1: raise ValueError("Only version 1 supported");

    # flags
    flags = parser.uleb()

    # proto+    
    proto_buffer = []
    while True:
        l = parser.uleb()
        proto_buffer.append(parser.next_bytes(l))
        if parser.bytes[parser.pos] == 0:
            break
    # 0U and EOF
    if parser.uleb() != 0: raise ValueError("Missing 0U at end of file");
    print(parser.pos, len(parser.bytes))
    if parser.pos < len(parser.bytes): raise ValueError(" bytes leftover");

def entry_point(argv):
    try:
        filename = argv[1]
    except IndexError:
        print "You must supply a filename"
        return 1
    parse(filename)
    return 0

def target(*args):
    return entry_point, None

if __name__ == "__main__":
    entry_point(sys.argv)
