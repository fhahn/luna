
class AbstractInstruction(object):
    def __init__(self, word):
        self.parse_args_a(word)

    def apply(self, interpreter):
        raise NotImplementedError

    def parse_args_b_c(self, word):
        self.b = (word >> 16) & 0xff
        self.c = word >> 24

    def parse_args_d(self, word):
        self.d = word >> 16

    def parse_args_a(self, word):
        self.a = (word >> 8) & 0xff



class ADInstruction(AbstractInstruction):
    def __init__(self, word):
        AbstractInstruction.__init__(self, word)
        self.parse_args_d(word)
    def tostr(self):
        return "%s A: %s  D: %s" %(self.name(), self.a, self.d)

class KSHORT(ADInstruction):
    def apply(self, interpreter):
        print(self.tostr())
        return 0

    def name(self):
        return 'KSHORT'

class GSET(ADInstruction):
    def apply(self, interpreter):
        print(self.tostr())
        return 0

    def name(self):
        return 'GSET'

class RET0(ADInstruction):
    def apply(self, interpreter):
        print(self.tostr())
        return 1

    def name(self):
        return 'RET0'


class ISLT(AbstractInstruction): pass


class ISGE(AbstractInstruction): pass


class ISLE(AbstractInstruction): pass


class ISGT(AbstractInstruction): pass


class ISEQV(AbstractInstruction): pass


class ISNEV(AbstractInstruction): pass


class ISEQS(AbstractInstruction): pass


class ISNES(AbstractInstruction): pass


class ISEQN(AbstractInstruction): pass


class ISNEN(AbstractInstruction): pass


class ISEQP(AbstractInstruction): pass


class ISNEP(AbstractInstruction): pass


class ISTC(AbstractInstruction): pass


class ISFC(AbstractInstruction): pass


class IST(AbstractInstruction): pass


class ISF(AbstractInstruction): pass


class MOV(AbstractInstruction): pass


class NOT(AbstractInstruction): pass


class UNM(AbstractInstruction): pass


class LEN(AbstractInstruction): pass


class ADDVN(AbstractInstruction): pass


class SUBVN(AbstractInstruction): pass


class MULVN(AbstractInstruction): pass


class DIVVN(AbstractInstruction): pass


class MODVN(AbstractInstruction): pass


class ADDNV(AbstractInstruction): pass


class SUBNV(AbstractInstruction): pass


class MULNV(AbstractInstruction): pass


class DIVNV(AbstractInstruction): pass


class MODNV(AbstractInstruction): pass


class ADDVV(AbstractInstruction): pass


class SUBVV(AbstractInstruction): pass


class MULVV(AbstractInstruction): pass


class DIVVV(AbstractInstruction): pass


class MODVV(AbstractInstruction): pass


class POW(AbstractInstruction): pass


class CAT(AbstractInstruction): pass


class KSTR(AbstractInstruction): pass


class KCDATA(AbstractInstruction): pass



class KNUM(AbstractInstruction): pass


class KPRI(AbstractInstruction): pass


class KNIL(AbstractInstruction): pass


class UGET(AbstractInstruction): pass


class USETV(AbstractInstruction): pass


class USETS(AbstractInstruction): pass


class USETN(AbstractInstruction): pass


class USETP(AbstractInstruction): pass


class UCLO(AbstractInstruction): pass


class FNEW(AbstractInstruction): pass


class TNEW(AbstractInstruction): pass


class TDUP(AbstractInstruction): pass


class GGET(AbstractInstruction): pass


class TGETV(AbstractInstruction): pass


class TGETS(AbstractInstruction): pass


class TGETB(AbstractInstruction): pass


class TSETV(AbstractInstruction): pass


class TSETS(AbstractInstruction): pass


class TSETB(AbstractInstruction): pass


class TSETM(AbstractInstruction): pass


class CALLM(AbstractInstruction): pass


class CALL(AbstractInstruction): pass


class CALLMT(AbstractInstruction): pass


class CALLT(AbstractInstruction): pass


class ITERC(AbstractInstruction): pass


class ITERN(AbstractInstruction): pass


class VARG(AbstractInstruction): pass


class ISNEXT(AbstractInstruction): pass


class RETM(AbstractInstruction): pass


class RET(AbstractInstruction): pass


class RET1(AbstractInstruction): pass


class FORI(AbstractInstruction): pass


class JFORI(AbstractInstruction): pass


class FORL(AbstractInstruction): pass


class IFORL(AbstractInstruction): pass


class JFORL(AbstractInstruction): pass


class ITERL(AbstractInstruction): pass


class IITERL(AbstractInstruction): pass


class JITERL(AbstractInstruction): pass


class LOOP(AbstractInstruction): pass


class ILOOP(AbstractInstruction): pass


class JLOOP(AbstractInstruction): pass


class JMP(AbstractInstruction): pass


class FUNCF(AbstractInstruction): pass


class IFUNCF(AbstractInstruction): pass


class JFUNCF(AbstractInstruction): pass


class FUNCV(AbstractInstruction): pass


class IFUNCV(AbstractInstruction): pass


class JFUNCV(AbstractInstruction): pass


class FUNCC(AbstractInstruction): pass


class FUNCCW(AbstractInstruction): pass
