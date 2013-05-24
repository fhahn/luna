from pylua.opcodes import unrolled_op_desc
from pylua.objspace import ObjectSpace
from pylua.helpers import debug_print, W_Str, W_Num, W_Object, W_Func, W_Pri



class SReturnValue(object):
    """Signals a 'return' statement.
    Argument is the wrapped object to return."""
    _immutable_ = True

    def __init__(self, returnvalue):
        self.returnvalue = returnvalue


class LuaFrame(object):
    def __init__(self, flags, constants, instructions):
        self.flags = flags
        self.constants = constants
        self.num_constants = len(constants)
        self.instructions = instructions
        self.num_instructions = len(instructions)
        # TODO check bounds
        self.space = ObjectSpace()

        self.registers = [W_Object()] * 10
        self.cmp_result = False


class LuaBuiltinFrame(LuaFrame):
    def __init__(self, function):
        self.function = function

    def call1(self, arg):
        self.function(arg)


class LuaBytecodeFrame(LuaFrame):

    def execute_frame(self, space):
        next_instr = 0
        self.space = space
        while True:
            i_opcode, i_args = self.instructions[next_instr]

            for op_desc in unrolled_op_desc:
                if i_opcode == op_desc.index:
                    meth = getattr(self, op_desc.name)
                    res = meth(i_args)
                    if op_desc.name in ('RET0', 'RET1', 'RET'):
                        ret_val = SReturnValue(res)
                        return ret_val
                    # TODO: return -1 everywhere
                    if res is None or res == -1:
                        next_instr += 1
                    else:
                        next_instr += res

            if next_instr >= self.num_instructions: break

    def decode_lits(self, val):
        return 0x10000 - val if (val & 0x8000) > 0 else val

    def get_str_constant(self, val):
        w_v = self.constants[self.num_constants-val-1]
        assert isinstance(w_v, W_Str)
        return w_v

    def get_num_constant(self, val):
        w_v = self.constants[val]
        assert isinstance(w_v, W_Num)
        return w_v.getval()

    def ISLT(self, args): raise NotImplementedError('ISLT not implemented') 

    def ISGE(self, args): raise NotImplementedError('ISGE not implemented') 

    def ISLE(self, args): raise NotImplementedError('ISLE not implemented') 

    def ISGT(self, args): raise NotImplementedError('ISGT not implemented') 

    def ISEQV(self, args):
        """
        A: var, D: var
        A == D
        """
        w_x = self.registers[args[0]]
        w_y = self.registers[args[1]]
        self.cmp_result = w_x.eq(w_y)

    def ISNEV(self, args):
        """
        A: var, D: var
        A != D
        """
        w_x = self.registers[args[0]]
        w_y = self.registers[args[1]]
        self.cmp_result = w_x.neq(w_y)

    def ISEQS(self, args):
        """
        A: var, D: str
        A == D
        """
        w_var = self.registers[args[0]]
        w_str = self.get_str_constant(args[1])
        self.cmp_result = w_var.eq(w_str) 

    def ISNES(self, args):
        """
        A: var, D: str
        A != D
        """
        w_var = self.registers[args[0]]
        w_str = self.get_str_constant(args[1])
        self.cmp_result = w_var.neq(w_str) 

    def ISEQN(self, args):
        """
        A: var, D: num
        """
        w_var = self.registers[args[0]]
        w_num = self.constants[args[1]]
        self.cmp_result = w_var.eq(w_num) 

    def ISNEN(self, args):
        """
        A: var, D: num
        """
        w_var = self.registers[args[0]]
        w_num = self.constants[args[1]]
        self.cmp_result = w_var.neq(w_num)

    def ISEQP(self, args):
        """
        A: var, D: pri
        A == D
        """
        w_var = self.registers[args[0]]
        w_pri = W_Pri(args[1])
        self.cmp_result = w_var.eq(w_pri)

    def ISNEP(self, args):
        """
        A: var, D: pri
        A != D
        """
        w_var = self.registers[args[0]]
        w_pri = W_Pri(args[1])
        self.cmp_result = w_var.neq(w_pri)

    def ISTC(self, args): raise NotImplementedError('ISTC not implemented') 

    def ISFC(self, args): raise NotImplementedError('ISFC not implemented') 

    def IST(self, args): raise NotImplementedError('IST not implemented') 

    def ISF(self, args): raise NotImplementedError('ISF not implemented') 

    def MOV(self, args): raise NotImplementedError('MOV not implemented') 

    def NOT(self, args): raise NotImplementedError('NOT not implemented') 

    def UNM(self, args): raise NotImplementedError('UNM not implemented') 

    def LEN(self, args): raise NotImplementedError('LEN not implemented') 

    def ADDVN(self, args):
        """
        A: dst, B: var, C: num
        """
        w_v1 = self.registers[args[1]]
        assert isinstance(w_v1, W_Num)
        v1 = w_v1.getval()
        v2 = self.get_num_constant(args[2])
        debug_print("ADDVN: Reg[%s] = %s + %s" % (args[0], v1, v2))
        self.registers[args[0]] = W_Num(v1 + v2)

    def SUBVN(self, args): raise NotImplementedError('SUBVN not implemented') 

    def MULVN(self, args): raise NotImplementedError('MULVN not implemented') 

    def DIVVN(self, args): raise NotImplementedError('DIVVN not implemented') 

    def MODVN(self, args): raise NotImplementedError('MODVN not implemented') 

    def ADDNV(self, args): raise NotImplementedError('ADDNV not implemented') 

    def SUBNV(self, args): raise NotImplementedError('SUBNV not implemented') 

    def MULNV(self, args): raise NotImplementedError('MULNV not implemented') 

    def DIVNV(self, args): raise NotImplementedError('DIVNV not implemented') 

    def MODNV(self, args): raise NotImplementedError('MODNV not implemented') 

    def ADDVV(self, args):
        """
        A: dst, B: var, C: var
        Sets A to B + C
        """
        w_v1 = self.registers[args[1]]
        assert isinstance(w_v1, W_Num)
        w_v2 = self.registers[args[2]]
        assert isinstance(w_v2, W_Num)
        v1 = w_v1.getval()
        v2 = w_v2.getval()
        debug_print("ADDVV: Reg %d = %s + %s" % (args[0], v1, v2))
        self.registers[args[0]] = W_Num(v1 + v2)

    def SUBVV(self, args): raise NotImplementedError('SUBVV not implemented') 

    def MULVV(self, args): raise NotImplementedError('MULVV not implemented') 

    def DIVVV(self, args): raise NotImplementedError('DIVVV not implemented') 

    def MODVV(self, args): raise NotImplementedError('MODVV not implemented') 

    def POW(self, args): raise NotImplementedError('POW not implemented') 

    def CAT(self, args): raise NotImplementedError('CAT not implemented') 

    def KSTR(self, args):
        """
        A: dst, D: str
        Set register A to str
        """
        w_str = self.get_str_constant(args[1])
        self.registers[args[0]] = w_str

    def KCDATA(self, args): raise NotImplementedError('KCDATA not implemented') 

    def KSHORT(self, args): 
        """
        A: dst, D: lits
        Set A to 16 bit signed integer D
        """
        val = self.decode_lits(args[1])
        debug_print("KSHORT: set R %d to %d" %(args[0], val))
        self.registers[args[0]] = W_Num(val)

    def KNUM(self, args):
        """
        A: dst, D: num
        Set A to number constant D
        """
        val = self.get_num_constant(args[1])
        self.registers[args[0]] = W_Num(val)

    def KPRI(self, args):
        """
        A: dst, D pri
        sets dst register to pri
        """
        self.registers[args[0]] = W_Pri(args[1])

    def KNIL(self, args): raise NotImplementedError('KNIL not implemented') 

    def UGET(self, args): raise NotImplementedError('UGET not implemented') 

    def USETV(self, args): raise NotImplementedError('USETV not implemented') 

    def USETS(self, args): raise NotImplementedError('USETS not implemented') 

    def USETN(self, args): raise NotImplementedError('USETN not implemented') 

    def USETP(self, args): raise NotImplementedError('USETP not implemented') 

    def UCLO(self, args): raise NotImplementedError('UCLO not implemented') 

    def FNEW(self, args): raise NotImplementedError('FNEW not implemented') 

    def TNEW(self, args): raise NotImplementedError('TNEW not implemented') 

    def TDUP(self, args): raise NotImplementedError('TDUP not implemented') 

    def GGET(self, args):
       """
       A: dst, D: str
       get global
       """
       key = self.get_str_constant(args[1]).getval()
       debug_print("GGET: get %s in R %s" % (key, args[0]))
       self.registers[args[0]] = self.space.globals[key]

    def GSET(self, args):
        """
        A: dst, D: str
        Set Global
        """
        key = self.get_str_constant(args[1]).getval()
        val = self.registers[args[0]]
        debug_print('GSET: set global %s to %s' %(key, val))
        self.space.globals[key] = val

    def TGETV(self, args): raise NotImplementedError('TGETV not implemented') 

    def TGETS(self, args): raise NotImplementedError('TGETS not implemented') 

    def TGETB(self, args): raise NotImplementedError('TGETB not implemented') 

    def TSETV(self, args): raise NotImplementedError('TSETV not implemented') 

    def TSETS(self, args): raise NotImplementedError('TSETS not implemented') 

    def TSETB(self, args): raise NotImplementedError('TSETB not implemented') 

    def TSETM(self, args): raise NotImplementedError('TSETM not implemented') 

    def CALLM(self, args): raise NotImplementedError('CALLM not implemented') 

    def CALL(self, args):
        w_func = self.registers[args[0]]
        assert isinstance(w_func, W_Func)
        func = w_func.getval()
        func.call1(self.registers[args[0]+1])

    def CALLMT(self, args): raise NotImplementedError('CALLMT not implemented') 

    def CALLT(self, args): raise NotImplementedError('CALLT not implemented') 

    def ITERC(self, args): raise NotImplementedError('ITERC not implemented') 

    def ITERN(self, args): raise NotImplementedError('ITERN not implemented') 

    def VARG(self, args): raise NotImplementedError('VARG not implemented') 

    def ISNEXT(self, args): raise NotImplementedError('ISNEXT not implemented') 

    def RETM(self, args): raise NotImplementedError('RETM not implemented') 

    def RET(self, args): raise NotImplementedError('RET not implemented') 

    def RET0(self, args): 
        """
        A: rbase, D: lit
        Return without value
        """
        debug_print("RET0 called")
        return 0

    def RET1(self, args):
        """
        A: rbase, D: lit
        Return with exactly one value, R(A) holds the value
        """
        # TODO only numbers at the moment
 
        w_v = self.registers[args[0]]
        assert isinstance(w_v, W_Num)
        retval = w_v.getval()
        debug_print('RET1: return %s' % retval)
        return retval

    def FORI(self, args): raise NotImplementedError('FORI not implemented') 

    def JFORI(self, args): raise NotImplementedError('JFORI not implemented') 

    def FORL(self, args): raise NotImplementedError('FORL not implemented') 

    def IFORL(self, args): raise NotImplementedError('IFORL not implemented') 

    def JFORL(self, args): raise NotImplementedError('JFORL not implemented') 

    def ITERL(self, args): raise NotImplementedError('ITERL not implemented') 

    def IITERL(self, args): raise NotImplementedError('IITERL not implemented') 

    def JITERL(self, args): raise NotImplementedError('JITERL not implemented') 

    def LOOP(self, args): raise NotImplementedError('LOOP not implemented') 

    def ILOOP(self, args): raise NotImplementedError('ILOOP not implemented') 

    def JLOOP(self, args): raise NotImplementedError('JLOOP not implemented') 

    def JMP(self, args): 
        """
        A: Rbase, D: jmp (next instr)
        """
        if self.cmp_result:
            # TODO find out about the offset
            return args[1] - 32768 + 1
        else:
            # rpython does not like returning None here
            return -1

    def FUNCF(self, args): raise NotImplementedError('FUNCF not implemented') 

    def IFUNCF(self, args): raise NotImplementedError('IFUNCF not implemented') 

    def JFUNCF(self, args): raise NotImplementedError('JFUNCF not implemented') 

    def FUNCV(self, args): raise NotImplementedError('FUNCV not implemented') 

    def IFUNCV(self, args): raise NotImplementedError('IFUNCV not implemented') 

    def JFUNCV(self, args): raise NotImplementedError('JFUNCV not implemented') 

    def FUNCC(self, args): raise NotImplementedError('FUNCC not implemented') 

    def FUNCCW(self, args): raise NotImplementedError('FUNCCW not implemented') 
