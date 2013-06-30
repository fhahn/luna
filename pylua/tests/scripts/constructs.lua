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

local a,b = 1,nil;
assert(-(1 or 2) == -1 and (1 and 2)+(-1.25 or -4) == 0.75);
x = ((b or a)+1 == 2 and (10 or a)+1 == 11); assert(x);
x = (((2<3) or 1) == true and (2<3 and 4) == 4); assert(x);

x,y=1,2;
assert((x>y) and x or y == 2);
x,y=2,1;
assert((x>y) and x or y == 2);

assert(1234567890 == tonumber('1234567890') and 1234567890+1 == 1234567891)


-- silly loops
repeat until 1; repeat until true;
while false do end; while nil do end;

do  -- test old bug (first name could not be an `upvalue')
 local a; function f(x) x={a=1}; x={x=1}; x={G=1} end
end

function f (i)
  if type(i) ~= 'number' then return i,'jojo'; end;
  if i > 0 then return i, f(i-1); end;
end
x = {f(3), f(5), f(10);};
--for key,value in pairs(x) do print(key,value) end
assert(x[1] == 3 and x[2] == 5 and x[3] == 10 and x[4] == 9 and x[12] == 1);
assert(x[nil] == nil)
x = {f'alo', f'xixi', nil};
assert(x[1] == 'alo' and x[2] == 'xixi' and x[3] == nil);
x = {f'alo'..'xixi'};
assert(x[1] == 'aloxixi')
x = {f{}}
assert(x[2] == 'jojo' and type(x[1]) == 'table')

local f = function (i)
  if i < 10 then return 'a';
  elseif i < 20 then return 'b';
  elseif i < 30 then return 'c';
  end;
end

assert(f(3) == 'a' and f(12) == 'b' and f(26) == 'c' and f(100) == nil)

for i=1,1000 do break; end;
n=100;
i=3;
t = {};
a=nil
while not a do
  a=0; for i=1,n do for i=i,1,-1 do a=a+1; t[i]=1; end; end;
end
assert(a == n*(n+1)/2 and i==3);
assert(t[1] and t[n] and not t[0] and not t[n+1])

print("OK")
