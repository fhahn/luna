print "testing syntax"

-- testing priorities

assert(2^3^2 == 2^(3^2));
assert(2^3*4 == (2^3)*4);
assert(2^-2 == 1/4 and -2^- -2 == - - -4);
assert(not nil and 2 and not(2>3 or 3<2));
assert(-3-1-5 == 0+0-9);
assert(-2^2 == -4 and (-2)^2 == 4 and 2*2-3-1 == 0);
assert(2*1+3/3 == 3 and 1+2 .. 3*1 == "33");
assert(not(2+1 > 3*1) and "a".."b" > "a");

assert(not ((true or false) and nil))
assert(      true or false  and nil)


print'OK'
