from rpython.rlib.rstruct.ieee import pack_float
from rpython.rlib.rstruct.runpack import runpack
from pylua.opcodes import unrolled_op_desc
from pylua.helpers import debug_print
from pylua.w_objects import W_Str, W_Num, W_Object, W_Pri, W_Table


class LuaFrame(W_Object):
    def __init__(self, flags, constants, instructions):
        self.flags = flags
        self.constants = constants
        self.num_constants = len(constants)
        self.instructions = instructions
        self.num_instructions = len(instructions)
        self.cmp_result = False
        self.registers = [W_Pri(0)] * 50
        self.multires = []

    def getval(self):
        return self


class LuaBuiltinFrame(LuaFrame):
    def __init__(self, function):
        self.function = function
        self.registers = []

    def call(self, args, space):
        return self.function(args)

    def clone(self):
        # no need to cleon, LuaBuilinFrame has no state
        return self


class LuaBytecodeFrame(LuaFrame):
    def execute_frame(self, space):
        next_instr = 0
        self.space = space
        while True:
            i_opcode, i_args = self.instructions[next_instr]

            for op_desc in unrolled_op_desc:
                if i_opcode == op_desc.index:
                    meth = getattr(self, op_desc.name)
                    res = meth(i_args, space)
                    if op_desc.name in ('RET0', 'RET1', 'RET', 'RETM', 'CALLT'):
                        return res
                    # TODO: return -1 everywhere
                    if res is None or res == -1:
                        next_instr += 1
                    else:
                        next_instr += res

            if next_instr >= self.num_instructions:
                break

    def decode_lits(self, val):
        return val - 0x10000 if (val & 0x8000) > 0 else val

    def get_str_constant(self, val):
        w_v = self.constants[self.num_constants-val-1]
        return w_v

    def get_func_constant(self, val):
        w_v = self.constants[self.num_constants-val-1]
        assert isinstance(w_v, LuaFrame)
        return w_v

    def get_num_constant(self, val):
        return self.constants[val].n_val

    def get_num_register(self, pos):
        return self.registers[pos].n_val

    def get_tab_constant(self, val):
        return self.constants[self.num_constants-1-val]

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
        if w_var is not None:
            self.cmp_result = w_var.eq(w_str)
        else:
            self.cmp_result = False

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

    def ISTC(self, args, space):
        """
        A: dst, D: var
        Copy D to A and jump, if D is true
        """
        w_var = self.registers[args[1]]
        self.registers[args[0]] = w_var.clone()
        self.cmp_result = w_var.is_true()

    def ISFC(self, args, space): raise NotImplementedError('ISFC not implemented') 

    def IST(self, args, space):
        """
        A: , D:var
        Jump if D is true
        """
        w_var = self.registers[args[1]]
        self.cmp_result = w_var.is_true()

    def ISF(self, args, space):
        """
        A: , D:var
        Jump if D is false
        """
        w_var = self.registers[args[1]]
        self.cmp_result = not w_var.is_true()

    def MOV(self, args, space):
        w_var = self.registers[args[1]]
        if not isinstance(w_var, W_Table) and not isinstance(w_var, LuaBytecodeFrame):
            w_var = w_var.clone()
        self.registers[args[0]] = w_var

    def NOT(self, args, space):
        """
        A:dst, D: var
        Set A to boolean not of D
        """
        w_var = self.registers[args[1]]
        if w_var.is_true():
            self.registers[args[0]] = W_Pri(1)
        else:
            self.registers[args[0]] = W_Pri(2)

    def UNM(self, args, space):
        """
        A: dst, D: var
        Set A to -D (unary minus)
        """
        w_var = self.registers[args[1]]
        assert isinstance(w_var, W_Num)
        self.registers[args[0]] = W_Num(-w_var.n_val)

    def LEN(self, args, space):
        w_var = self.registers[args[1]]
        if isinstance(w_var, W_Table):
            l = len(w_var.content)
            w_first = w_var.get(W_Num(0))
            try:
                w_v = w_var.content[W_Num(0).hash()]
                if isinstance(w_v, W_Pri) and w_v.n_val == 0:
                    l -= 1
            except KeyError:
                pass
            self.registers[args[0]] = W_Num(l)
        else:
            raise NotImplementedError('Len for types other than table not supported atm')

    def ADDVN(self, args, space):
        """
        A: dst, B: var, C: num
        """
        v1 = self.get_num_register(args[1])
        v2 = self.get_num_constant(args[2])
        debug_print("ADDVN: Reg[%s] = %s + %s" % (args[0], v1, v2))
        self.registers[args[0]] = W_Num(v1+v2)

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
        v1 = self.get_num_constant(args[2])
        v2 = self.get_num_register(args[1])
        self.registers[args[0]] = W_Num(v1+v2)

    def SUBNV(self, args, space):
        v1 = self.get_num_constant(args[2])
        v2 = self.get_num_register(args[1])
        self.registers[args[0]] = W_Num(v1-v2)

    def MULNV(self, args, space):
        v1 = self.get_num_constant(args[2])
        v2 = self.get_num_register(args[1])
        self.registers[args[0]] = W_Num(v1*v2)

    def DIVNV(self, args, space):
        v1 = self.get_num_constant(args[2])
        v2 = self.get_num_register(args[1])
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

    def CAT(self, args, space):
        """
        A: dst, B: rbase, C: rbase
        concat strings from b to c
        """
        
        strs = []
        for i in xrange(args[1], args[2]+1):
            strs.append(self.registers[i].to_str())
        self.registers[args[0]] = W_Str(''.join(strs))

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

    def KNIL(self, args, space):
        """
        A: base, D: base
        Set slots A to D to nil
        """
        for i in xrange(0, args[1]-args[0]+1):
            self.registers[args[0]+i] = W_Pri(0)

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

    def TNEW(self, args, space): 
        # ignore table size at the moment
        self.registers[args[0]] = W_Table()

    def TDUP(self, args, space):
        w_table = self.get_tab_constant(args[1])
        assert isinstance(w_table, W_Table)
        self.registers[args[0]] = w_table.clone()

    def GGET(self, args, space):
       """
       A: dst, D: str
       get global
       """
       key = self.get_str_constant(args[1]).s_val
       debug_print("GGET: get %s in R %s" % (key, args[0]))
       self.registers[args[0]] = space.globals[key]

    def GSET(self, args, space):
        """
        A: dst, D: str
        Set Global
        """
        key = self.get_str_constant(args[1]).s_val
        val = self.registers[args[0]]
        debug_print('GSET: set global %s to %s' %(key, val))
        self.space.globals[key] = val

    def TGETV(self, args, space):
        w_t = self.registers[args[1]]
        assert isinstance(w_t, W_Table)
        w_key = self.registers[args[2]]
        self.registers[args[0]] = w_t.get(w_key)

    def TGETS(self, args, space):
        w_t = self.registers[args[1]]
        assert isinstance(w_t, W_Table)
        w_key = self.get_str_constant(args[2])
        self.registers[args[0]] = w_t.get(w_key)

    def TGETB(self, args, space):
        w_t = self.registers[args[1]]
        assert isinstance(w_t, W_Table)
        # TODO: we must wrap ints into W_Num because set
        # expects a W_Object as key
        self.registers[args[0]] = w_t.get(W_Num(args[2]))

    def TSETV(self, args, space):
        w_t = self.registers[args[1]]
        assert isinstance(w_t, W_Table)
        w_key = self.registers[args[2]]
        w_t.set(w_key, self.registers[args[0]])

    def TSETS(self, args, space):
        w_t = self.registers[args[1]]
        assert isinstance(w_t, W_Table)
        w_key = self.get_str_constant(args[2])
        w_t.set(w_key, self.registers[args[0]])

    def TSETB(self, args, space):
        w_t = self.registers[args[1]]
        assert isinstance(w_t, W_Table)
        # TODO: we must wrap ints into W_Num because set
        # expects a W_Object as key
        w_t.set(W_Num(args[2]), self.registers[args[0]])
 
    def TSETM(self, args, space):
        """
        A: base, D: *num
        (A-1)[D], (A-1)[D+1], ... = A, A+1, ...

        *num is the index to a num constant that's a float
        only use first 32 bit of mantissa
        """
        w_table = self.registers[args[0]-1]
        index = self.get_num_constant(args[1])
        packed = []
        pack_float(packed, index, 8, True)
        index = runpack('>i', packed[0][4:])
        for i in xrange(0, len(self.multires)):
            w_table.set(W_Num(index+i), self.multires[i])

    def CALLM(self, args, space): raise NotImplementedError('CALLM not implemented') 

    def CALL(self, args, space):
        """
        A: base, B: lit, C: lit
        Call: A, ..., A+B-2 = A(A+1, ..., A+C-1)
        """
        w_func = self.registers[args[0]]
        # clone the frame, so every frame has it's own registers
        # because a frame can be called multiple times (recursion)
        if isinstance(w_func, LuaBytecodeFrame):
            old_regs = w_func.registers
            w_func.registers = [x for x in self.registers]
            j = 0
            for i in xrange(1, args[2]):
                w_func.registers[j] = self.registers[args[0]+i]
                j = j+1
            w_res = w_func.execute_frame(space)
            w_func.registers = old_regs
        elif isinstance(w_func, LuaBuiltinFrame):
            params = []
            for i in xrange(1, args[2]):
                w_param = self.registers[args[0]+i]
                if isinstance(w_param, W_Table):
                        # pass tables as reference
                    params.append(w_param)
                else:
                    params.append(w_param.clone())
            w_res = w_func.function(params)
        else:
            assert 0

        if args[1] == 0: # multires return
            self.multires = w_res
        else:
            # TODO: if args[1]-1 > len(w_res) overflow registers are not 
            #       set to nil
            for i in xrange(0, min(args[1]-1, len(w_res or []))):
                self.registers[args[0]+i] = w_res[i]

    def CALLMT(self, args, space): raise NotImplementedError('CALLMT not implemented') 

    def CALLT(self, args, space):
        w_func = self.registers[args[0]]
        # clone the frame, so every frame has it's own registers
        # because a frame can be called multiple times (recursion)
        if isinstance(w_func, LuaBytecodeFrame):
            old_regs = w_func.registers
            w_func.registers = list(old_regs)
            j = 0
            for i in xrange(1, args[1]):
                w_func.registers[j] = self.registers[args[0]+i]
                j = j+1
            w_res = w_func.execute_frame(space)
            w_func.registers = old_regs
        elif isinstance(w_func, LuaBuiltinFrame):
            w_res = w_func.function([self.registers[args[0]+i].clone() for i in xrange(1, args[1])])
        else:
            assert 0
        return w_res

    def ITERC(self, args, space): raise NotImplementedError('ITERC not implemented') 

    def ITERN(self, args, space): raise NotImplementedError('ITERN not implemented') 

    def VARG(self, args, space): raise NotImplementedError('VARG not implemented') 

    def ISNEXT(self, args, space): raise NotImplementedError('ISNEXT not implemented') 

    def RETM(self, args, space):
        """
        A: base, D: lit
        return A, ..., A+D+MULTRES-1
        """
        w_return_values = []
        for i in xrange(0, args[1]):
            w_return_values.append(self.registers[args[0]+i])

        w_return_values += self.multires
        return w_return_values


    def RET(self, args, space):
        """
        A: rbase, B: lit
        return A, ..., A+D-2
        """
        w_return_values = []
        for i in xrange(0, args[1]-1):
            w_return_values.append(self.registers[args[0]+i])
        return w_return_values

    def RET0(self, args, space): 
        """
        A: rbase, D: lit
        Return without value
        """
        debug_print("RET0 called")
        return [W_Num(0)]

    def RET1(self, args, space):
        """
        A: rbase, D: lit
        Return with exactly one value, R(A) holds the value
        """
        # TODO only numbers at the moment
        w_v = self.registers[args[0]]
        debug_print('RET1: return %s' % w_v.to_str())
        # TODO results are wrapped in a list, because it makes returning multiple arguments
        # easier, improve if possible
        return [w_v]

    def continue_for_loop(self, idx, stop, step):
        if step >= 0:
            return idx <= stop
        else:
            return idx >= stop

    def FORI(self, args, space):
        #TODO combine FORI and FORL?
        base = args[0]
        w_idx = self.registers[base]
        w_stop = self.registers[base+1]
        w_step = self.registers[base+2]
        self.registers[base+3] = w_idx.clone()
        if self.continue_for_loop(w_idx.n_val, w_stop.n_val, w_step.n_val):
            return 1
        else:
            return args[1] - 32768 + 1

    def JFORI(self, args, space): raise NotImplementedError('JFORI not implemented') 

    def FORL(self, args, space):
        base = args[0]
        w_idx = self.registers[base]
        w_stop = self.registers[base+1]
        w_step = self.registers[base+2]
        w_idx.n_val += w_step.n_val
        self.registers[base+3] = w_idx.clone()
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
