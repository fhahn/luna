

from rpython.rlib import jit

from pylua.opcodes import unrolled_op_desc

class LuaFrame(object):
    def __init__(self, flags, constants, instructions):
        self.flags = flags
        self.constants = constants
        self.instructions = instructions

    @jit.unroll_safe
    def execute_frame(self):
        pc = 0
        while True:
            i_opcode, i_args = self.instructions[pc]
            pc += 1

            for op_desc in unrolled_op_desc:   
                if i_opcode == op_desc.index:
                    meth = getattr(self, op_desc.name)
                    meth(i_args)

    def ISLT(self, args): raise NotImplementedError('ISLT not implemented') 

    def ISGE(self, args): raise NotImplementedError('ISGE not implemented') 

    def ISLE(self, args): raise NotImplementedError('ISLE not implemented') 

    def ISGT(self, args): raise NotImplementedError('ISGT not implemented') 

    def ISEQV(self, args): raise NotImplementedError('ISEQV not implemented') 

    def ISNEV(self, args): raise NotImplementedError('ISNEV not implemented') 

    def ISEQS(self, args): raise NotImplementedError('ISEQS not implemented') 

    def ISNES(self, args): raise NotImplementedError('ISNES not implemented') 

    def ISEQN(self, args): raise NotImplementedError('ISEQN not implemented') 

    def ISNEN(self, args): raise NotImplementedError('ISNEN not implemented') 

    def ISEQP(self, args): raise NotImplementedError('ISEQP not implemented') 

    def ISNEP(self, args): raise NotImplementedError('ISNEP not implemented') 

    def ISTC(self, args): raise NotImplementedError('ISTC not implemented') 

    def ISFC(self, args): raise NotImplementedError('ISFC not implemented') 

    def IST(self, args): raise NotImplementedError('IST not implemented') 

    def ISF(self, args): raise NotImplementedError('ISF not implemented') 

    def MOV(self, args): raise NotImplementedError('MOV not implemented') 

    def NOT(self, args): raise NotImplementedError('NOT not implemented') 

    def UNM(self, args): raise NotImplementedError('UNM not implemented') 

    def LEN(self, args): raise NotImplementedError('LEN not implemented') 

    def ADDVN(self, args): raise NotImplementedError('ADDVN not implemented') 

    def SUBVN(self, args): raise NotImplementedError('SUBVN not implemented') 

    def MULVN(self, args): raise NotImplementedError('MULVN not implemented') 

    def DIVVN(self, args): raise NotImplementedError('DIVVN not implemented') 

    def MODVN(self, args): raise NotImplementedError('MODVN not implemented') 

    def ADDNV(self, args): raise NotImplementedError('ADDNV not implemented') 

    def SUBNV(self, args): raise NotImplementedError('SUBNV not implemented') 

    def MULNV(self, args): raise NotImplementedError('MULNV not implemented') 

    def DIVNV(self, args): raise NotImplementedError('DIVNV not implemented') 

    def MODNV(self, args): raise NotImplementedError('MODNV not implemented') 

    def ADDVV(self, args): raise NotImplementedError('ADDVV not implemented') 

    def SUBVV(self, args): raise NotImplementedError('SUBVV not implemented') 

    def MULVV(self, args): raise NotImplementedError('MULVV not implemented') 

    def DIVVV(self, args): raise NotImplementedError('DIVVV not implemented') 

    def MODVV(self, args): raise NotImplementedError('MODVV not implemented') 

    def POW(self, args): raise NotImplementedError('POW not implemented') 

    def CAT(self, args): raise NotImplementedError('CAT not implemented') 

    def KSTR(self, args): raise NotImplementedError('KSTR not implemented') 

    def KCDATA(self, args): raise NotImplementedError('KCDATA not implemented') 

    def KSHORT(self, args): print("KSHORT called")

    def KNUM(self, args): raise NotImplementedError('KNUM not implemented') 

    def KPRI(self, args): raise NotImplementedError('KPRI not implemented') 

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

    def GGET(self, args): raise NotImplementedError('GGET not implemented') 

    def GSET(self, args): print("GSET called")

    def TGETV(self, args): raise NotImplementedError('TGETV not implemented') 

    def TGETS(self, args): raise NotImplementedError('TGETS not implemented') 

    def TGETB(self, args): raise NotImplementedError('TGETB not implemented') 

    def TSETV(self, args): raise NotImplementedError('TSETV not implemented') 

    def TSETS(self, args): raise NotImplementedError('TSETS not implemented') 

    def TSETB(self, args): raise NotImplementedError('TSETB not implemented') 

    def TSETM(self, args): raise NotImplementedError('TSETM not implemented') 

    def CALLM(self, args): raise NotImplementedError('CALLM not implemented') 

    def CALL(self, args): raise NotImplementedError('CALL not implemented') 

    def CALLMT(self, args): raise NotImplementedError('CALLMT not implemented') 

    def CALLT(self, args): raise NotImplementedError('CALLT not implemented') 

    def ITERC(self, args): raise NotImplementedError('ITERC not implemented') 

    def ITERN(self, args): raise NotImplementedError('ITERN not implemented') 

    def VARG(self, args): raise NotImplementedError('VARG not implemented') 

    def ISNEXT(self, args): raise NotImplementedError('ISNEXT not implemented') 

    def RETM(self, args): raise NotImplementedError('RETM not implemented') 

    def RET(self, args): raise NotImplementedError('RET not implemented') 

    def RET0(self, args): print("RET0 called")

    def RET1(self, args): raise NotImplementedError('RET1 not implemented') 

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

    def JMP(self, args): raise NotImplementedError('JMP not implemented') 

    def FUNCF(self, args): raise NotImplementedError('FUNCF not implemented') 

    def IFUNCF(self, args): raise NotImplementedError('IFUNCF not implemented') 

    def JFUNCF(self, args): raise NotImplementedError('JFUNCF not implemented') 

    def FUNCV(self, args): raise NotImplementedError('FUNCV not implemented') 

    def IFUNCV(self, args): raise NotImplementedError('IFUNCV not implemented') 

    def JFUNCV(self, args): raise NotImplementedError('JFUNCV not implemented') 

    def FUNCC(self, args): raise NotImplementedError('FUNCC not implemented') 

    def FUNCCW(self, args): raise NotImplementedError('FUNCCW not implemented')