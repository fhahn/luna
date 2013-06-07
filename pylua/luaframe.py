from pylua.opcodes import unrolled_op_desc
from pylua.objspace import ObjectSpace
from pylua.helpers import debug_print
from pylua.w_objects import W_Str, W_Num, W_Object, W_Func, W_Pri


class LuaFrame(W_Object):
    def __init__(self, flags, constants, instructions):
        self.flags = flags
        self.constants = constants
        self.num_constants = len(constants)
        self.instructions = instructions
        self.num_instructions = len(instructions)
        self.cmp_result = False
        self.registers = [W_Object()] * 10

    def getval(self):
        return self


class LuaBuiltinFrame(LuaFrame):
    def __init__(self, function):
        self.function = function

    def call0(self, space):
        # print specific
        return self.function(W_Str(''))

    def call1(self, arg, space):
        return self.function(arg)

    def clone(self):
        # no need to cleon, LuaBuilinFrame has no state
        return self


class LuaBytecodeFrame(LuaFrame):
    def call0(self, space):
        return self.execute_frame(space)

    def call1(self, arg, space):
        self.registers[0] = arg.clone()
        return self.execute_frame(space)

    def clone(self):
        return LuaBytecodeFrame(self.flags, self.constants, self.instructions)

    def execute_frame(self, space):
        next_instr = 0
        self.space = space
        while True:
            i_opcode, i_args = self.instructions[next_instr]

            for op_desc in unrolled_op_desc:
                if i_opcode == op_desc.index:
                    meth = getattr(self, op_desc.name)
                    res = meth(i_args, space)
                    if op_desc.name in ('RET0', 'RET1', 'RET'):
                        return res
                    # TODO: return -1 everywhere
                    if res is None or res == -1:
                        next_instr += 1
                    else:
                        next_instr += res

            if next_instr >= self.num_instructions: break

    def decode_lits(self, val):
        return val - 0x10000 if (val & 0x8000) > 0 else val

    def get_str_constant(self, val):
        w_v = self.constants[self.num_constants-val-1]
        assert isinstance(w_v, W_Str)
        return w_v

    def get_func_constant(self, val):
        w_v = self.constants[self.num_constants-val-1]
        assert isinstance(w_v, LuaFrame)
        return w_v


    def get_num_constant(self, val):
        w_v = self.constants[val]
        assert isinstance(w_v, W_Num)
        return w_v.getval()

    def get_num_register(self, pos):
        w_v = self.registers[pos]
        assert isinstance(w_v, W_Num)
        return w_v.getval()

    def ISLT(self, args, space):
        """
        A: var, D: var
        A < D
        """
        w_x = self.registers[args[0]]
        w_y = self.registers[args[1]]
        self.cmp_result = w_x.lt(w_y)

    def ISGE(self, args, space):
        """
        A: var, D: var
        A >= D
        """
        w_x = self.registers[args[0]]
        w_y = self.registers[args[1]]
        self.cmp_result = w_x.ge(w_y)

    def ISLE(self, args, space):
        """
        A: var, D: var
        A <= D
        """
        w_x = self.registers[args[0]]
        w_y = self.registers[args[1]]
        self.cmp_result = w_x.le(w_y)

    def ISGT(self, args, space):
        """
        A: var, D: var
        A > D
        """
        w_x = self.registers[args[0]]
        w_y = self.registers[args[1]]
        self.cmp_result = w_x.gt(w_y)
 
    def ISEQV(self, args, space):
        """
        A: var, D: var
        A == D
        """
        w_x = self.registers[args[0]]
        w_y = self.registers[args[1]]
        self.cmp_result = w_x.eq(w_y)

    def ISNEV(self, args, space):
        """
        A: var, D: var
        A != D
        """
        w_x = self.registers[args[0]]
        w_y = self.registers[args[1]]
        self.cmp_result = w_x.neq(w_y)

    def ISEQS(self, args, space):
        """
        A: var, D: str
        A == D
        """
        w_var = self.registers[args[0]]
        w_str = self.get_str_constant(args[1])
        self.cmp_result = w_var.eq(w_str) 

    def ISNES(self, args, space):
        """
        A: var, D: str
        A != D
        """
        w_var = self.registers[args[0]]
        w_str = self.get_str_constant(args[1])
        self.cmp_result = w_var.neq(w_str) 

    def ISEQN(self, args, space):
        """
        A: var, D: num
        """
        w_var = self.registers[args[0]]
        w_num = self.constants[args[1]]
        self.cmp_result = w_var.eq(w_num) 

    def ISNEN(self, args, space):
        """
        A: var, D: num
        """
        w_var = self.registers[args[0]]
        w_num = self.constants[args[1]]
        self.cmp_result = w_var.neq(w_num)

    def ISEQP(self, args, space):
        """
        A: var, D: pri
        A == D
        """
        w_var = self.registers[args[0]]
        w_pri = W_Pri(args[1])
        self.cmp_result = w_var.eq(w_pri)

    def ISNEP(self, args, space):
        """
        A: var, D: pri
        A != D
        """
        w_var = self.registers[args[0]]
        w_pri = W_Pri(args[1])
        self.cmp_result = w_var.neq(w_pri)

    def ISTC(self, args, space): raise NotImplementedError('ISTC not implemented') 

    def ISFC(self, args, space): raise NotImplementedError('ISFC not implemented') 

    def IST(self, args, space): raise NotImplementedError('IST not implemented') 

    def ISF(self, args, space): raise NotImplementedError('ISF not implemented') 

    def MOV(self, args, space):
        self.registers[args[0]] = self.registers[args[1]].clone()

    def NOT(self, args, space): raise NotImplementedError('NOT not implemented') 

    def UNM(self, args, space): raise NotImplementedError('UNM not implemented') 

    def LEN(self, args, space): raise NotImplementedError('LEN not implemented') 

    def ADDVN(self, args, space):
        """
        A: dst, B: var, C: num
        """
        v1 = self.get_num_register(args[1])
        v2 = self.get_num_constant(args[2])
        debug_print("ADDVN: Reg[%s] = %s + %s" % (args[0], v1, v2))
        self.registers[args[0]] = W_Num(v1 + v2)

    def SUBVN(self, args, space):
        """
        A: dst, B: var, C: num
        A = B + C
        """
        v1 = self.get_num_register(args[1])
        v2 = self.get_num_constant(args[2])
        self.registers[args[0]] = W_Num(v1 - v2)

    def MULVN(self, args, space):
        v1 = self.get_num_register(args[1])
        v2 = self.get_num_constant(args[2])
        self.registers[args[0]] = W_Num(v1*v2)

    def DIVVN(self, args, space):
        v1 = self.get_num_register(args[1])
        v2 = self.get_num_constant(args[2])
        self.registers[args[0]] = W_Num(v1/float(v2))

    def MODVN(self, args, space): raise NotImplementedError('MODVN not implemented') 

    def ADDNV(self, args, space):
        v1 = self.get_num_constant(args[1])
        v2 = self.get_num_register(args[2])
        self.registers[args[0]] = W_Num(v1+v2)

    def SUBNV(self, args, space):
        v1 = self.get_num_constant(args[1])
        v2 = self.get_num_register(args[2])
        self.registers[args[0]] = W_Num(v1-v2)

    def MULNV(self, args, space):
        v1 = self.get_num_constant(args[1])
        v2 = self.get_num_register(args[2])
        self.registers[args[0]] = W_Num(v1*v2)

    def DIVNV(self, args, space):
        v1 = self.get_num_constant(args[1])
        v2 = self.get_num_register(args[2])
        self.registers[args[0]] = W_Num(v1/float(v2))

    def MODNV(self, args, space): raise NotImplementedError('MODNV not implemented') 

    def ADDVV(self, args, space):
        """
        A: dst, B: var, C: var
        Sets A to B + C
        """
        v1 = self.get_num_register(args[1])
        v2 = self.get_num_register(args[2])
        debug_print("ADDVV: Reg %d = %s + %s" % (args[0], v1, v2))
        self.registers[args[0]] = W_Num(v1 + v2)

    def SUBVV(self, args, space):
        v1 = self.get_num_register(args[1])
        v2 = self.get_num_register(args[2])
        debug_print("ADDVV: Reg %d = %s + %s" % (args[0], v1, v2))
        self.registers[args[0]] = W_Num(v1-v2)

    def MULVV(self, args, space):
        v1 = self.get_num_register(args[1])
        v2 = self.get_num_register(args[2])
        self.registers[args[0]] = W_Num(v1*v2)

    def DIVVV(self, args, space):
        v1 = self.get_num_register(args[1])
        v2 = self.get_num_register(args[2])
        self.registers[args[0]] = W_Num(v1/float(v2))

    def MODVV(self, args, space): raise NotImplementedError('MODVV not implemented') 

    def POW(self, args, space): raise NotImplementedError('POW not implemented') 

    def CAT(self, args, space): raise NotImplementedError('CAT not implemented') 

    def KSTR(self, args, space):
        """
        A: dst, D: str
        Set register A to str
        """
        w_str = self.get_str_constant(args[1])
        self.registers[args[0]] = w_str

    def KCDATA(self, args, space): raise NotImplementedError('KCDATA not implemented') 

    def KSHORT(self, args, space): 
        """
        A: dst, D: lits
        Set A to 16 bit signed integer D
        """
        val = self.decode_lits(args[1])
        debug_print("KSHORT: set R %d to %d" %(args[0], val))
        self.registers[args[0]] = W_Num(val)

    def KNUM(self, args, space):
        """
        A: dst, D: num
        Set A to number constant D
        """
        val = self.get_num_constant(args[1])
        self.registers[args[0]] = W_Num(val)

    def KPRI(self, args, space):
        """
        A: dst, D pri
        sets dst register to pri
        """
        self.registers[args[0]] = W_Pri(args[1])

    def KNIL(self, args, space): raise NotImplementedError('KNIL not implemented') 

    def UGET(self, args, space): raise NotImplementedError('UGET not implemented') 

    def USETV(self, args, space): raise NotImplementedError('USETV not implemented') 

    def USETS(self, args, space): raise NotImplementedError('USETS not implemented') 

    def USETN(self, args, space): raise NotImplementedError('USETN not implemented') 

    def USETP(self, args, space): raise NotImplementedError('USETP not implemented') 

    def UCLO(self, args, space): 
        if args[0] != 0:
            raise NotImplementedError('Nonzero rbase not implemented') 
        else:
            return args[1] - 32768 + 1

    def FNEW(self, args, space):
        self.registers[args[0]]= self.get_func_constant(args[1])

    def TNEW(self, args, space): raise NotImplementedError('TNEW not implemented') 

    def TDUP(self, args, space): raise NotImplementedError('TDUP not implemented') 

    def GGET(self, args, space):
       """
       A: dst, D: str
       get global
       """
       key = self.get_str_constant(args[1]).getval()
       debug_print("GGET: get %s in R %s" % (key, args[0]))
       self.registers[args[0]] = space.globals[key]

    def GSET(self, args, space):
        """
        A: dst, D: str
        Set Global
        """
        key = self.get_str_constant(args[1]).getval()
        val = self.registers[args[0]]
        debug_print('GSET: set global %s to %s' %(key, val))
        self.space.globals[key] = val

    def TGETV(self, args, space): raise NotImplementedError('TGETV not implemented') 

    def TGETS(self, args, space): raise NotImplementedError('TGETS not implemented') 

    def TGETB(self, args, space): raise NotImplementedError('TGETB not implemented') 

    def TSETV(self, args, space): raise NotImplementedError('TSETV not implemented') 

    def TSETS(self, args, space): raise NotImplementedError('TSETS not implemented') 

    def TSETB(self, args, space): raise NotImplementedError('TSETB not implemented') 

    def TSETM(self, args, space): raise NotImplementedError('TSETM not implemented') 

    def CALLM(self, args, space): raise NotImplementedError('CALLM not implemented') 

    def CALL(self, args, space):
        w_func = self.registers[args[0]]
        assert isinstance(w_func, LuaFrame)
        # clone the frame, so every frame has it's own registers
        # because a frame can be called multiple times (recursion)
        func = w_func.getval().clone()

        if args[2] == 1: # 0 arguments
            w_res = func.call0(space)
        elif args[2] == 2: # 1 argument
            w_res = func.call1(self.registers[args[0]+1], space)
        else:
            w_res = W_Object()

        if args[1] == 1: #no return values
            pass
        elif args[1] == 2: # 1 return values
            self.registers[args[0]] = w_res

    def CALLMT(self, args, space): raise NotImplementedError('CALLMT not implemented') 

    def CALLT(self, args, space): raise NotImplementedError('CALLT not implemented') 

    def ITERC(self, args, space): raise NotImplementedError('ITERC not implemented') 

    def ITERN(self, args, space): raise NotImplementedError('ITERN not implemented') 

    def VARG(self, args, space): raise NotImplementedError('VARG not implemented') 

    def ISNEXT(self, args, space): raise NotImplementedError('ISNEXT not implemented') 

    def RETM(self, args, space): raise NotImplementedError('RETM not implemented') 

    def RET(self, args, space): raise NotImplementedError('RET not implemented') 

    def RET0(self, args, space): 
        """
        A: rbase, D: lit
        Return without value
        """
        debug_print("RET0 called")
        return W_Num(0)

    def RET1(self, args, space):
        """
        A: rbase, D: lit
        Return with exactly one value, R(A) holds the value
        """
        # TODO only numbers at the moment
        w_v = self.registers[args[0]]
        debug_print('RET1: return %s' % w_v.to_str())
        return w_v

    def continue_for_loop(self, idx, stop, step):
        if step >= 0:
            return idx <= stop
        else:
            return idx >= stop

    def FORI(self, args, space):
        #TODO combine FORI and FORL?
        base = args[0]
        w_idx = self.registers[base]
        assert isinstance(w_idx, W_Num)
        w_stop = self.registers[base+1]
        assert isinstance(w_stop, W_Num)
        w_step = self.registers[base+2]
        assert isinstance(w_step, W_Num)
        if self.continue_for_loop(w_idx.n_val, w_stop.n_val, w_step.n_val):
            return 1
        else:
            return args[1] - 32768 + 1

    def JFORI(self, args, space): raise NotImplementedError('JFORI not implemented') 

    def FORL(self, args, space):
        base = args[0]
        w_idx = self.registers[base]
        assert isinstance(w_idx, W_Num)
        w_stop = self.registers[base+1]
        assert isinstance(w_stop, W_Num)
        w_step = self.registers[base+2]
        assert isinstance(w_step, W_Num)
        w_idx.n_val += w_step.n_val
        if self.continue_for_loop(w_idx.n_val, w_stop.n_val, w_step.n_val):
            return args[1] - 32768 + 1
        else:
            return 1

    def IFORL(self, args, space): raise NotImplementedError('IFORL not implemented') 

    def JFORL(self, args, space): raise NotImplementedError('JFORL not implemented') 

    def ITERL(self, args, space): raise NotImplementedError('ITERL not implemented') 

    def IITERL(self, args, space): raise NotImplementedError('IITERL not implemented') 

    def JITERL(self, args, space): raise NotImplementedError('JITERL not implemented') 

    def LOOP(self, args, space): 
        """
        No Op, but can be used as loop hint for the jit in future
        """
        pass

    def ILOOP(self, args, space): raise NotImplementedError('ILOOP not implemented') 

    def JLOOP(self, args, space): raise NotImplementedError('JLOOP not implemented') 

    def JMP(self, args, space): 
        """
        A: Rbase, D: jmp (next instr)
        """
        if self.cmp_result:
            return args[1] - 32768 + 1
        else:
            # rpython does not like returning None here
            self.cmp_result = True
            return -1

    def FUNCF(self, args, space): raise NotImplementedError('FUNCF not implemented') 

    def IFUNCF(self, args, space): raise NotImplementedError('IFUNCF not implemented') 

    def JFUNCF(self, args, space): raise NotImplementedError('JFUNCF not implemented') 

    def FUNCV(self, args, space): raise NotImplementedError('FUNCV not implemented') 

    def IFUNCV(self, args, space): raise NotImplementedError('IFUNCV not implemented') 

    def JFUNCV(self, args, space): raise NotImplementedError('JFUNCV not implemented') 

    def FUNCC(self, args, space): raise NotImplementedError('FUNCC not implemented') 

    def FUNCCW(self, args, space): raise NotImplementedError('FUNCCW not implemented') 
