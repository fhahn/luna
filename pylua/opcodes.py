from rpython.rlib.unroll import unrolling_iterable

OP_DESC = [None] * 93 

class OpCodeDescritption(object):
    def __init__(self, name, index, args_type):
        self.name = name
        self.index = index
        self.args_type = args_type

    def _freeze_(self):
        return True

def def_op(name, index, args_type):
    OP_DESC[index] = OpCodeDescritption(name, index, args_type)

ARGS_AD = 0
ARGS_ABC = 1

def_op('ISLT', 0, ARGS_AD)

def_op('ISGE', 1, ARGS_AD)

def_op('ISLE', 2, ARGS_AD)

def_op('ISGT', 3, ARGS_AD)

def_op('ISEQV', 4, ARGS_AD)

def_op('ISNEV', 5, ARGS_AD)

def_op('ISEQS', 6, ARGS_AD)

def_op('ISNES', 7, ARGS_AD)

def_op('ISEQN', 8, ARGS_AD)

def_op('ISNEN', 9, ARGS_AD)

def_op('ISEQP', 10, ARGS_AD)

def_op('ISNEP', 11, ARGS_AD)

def_op('ISTC', 12, ARGS_AD)

def_op('ISFC', 13, ARGS_AD)

def_op('IST', 14, ARGS_AD)

def_op('ISF', 15, ARGS_AD)

def_op('MOV', 16, ARGS_AD)

def_op('NOT', 17, ARGS_AD)

def_op('UNM', 18, ARGS_AD)

def_op('LEN', 19, ARGS_AD)

def_op('ADDVN', 20, ARGS_ABC)

def_op('SUBVN', 21, ARGS_ABC)

def_op('MULVN', 22, ARGS_ABC)

def_op('DIVVN', 23, ARGS_ABC)

def_op('MODVN', 24, ARGS_ABC)

def_op('ADDNV', 25, ARGS_ABC)

def_op('SUBNV', 26, ARGS_ABC)

def_op('MULNV', 27, ARGS_ABC)

def_op('DIVNV', 28, ARGS_ABC)

def_op('MODNV', 29, ARGS_ABC)

def_op('ADDVV', 30, ARGS_ABC)

def_op('SUBVV', 31, ARGS_ABC)

def_op('MULVV', 32, ARGS_ABC)

def_op('DIVVV', 33, ARGS_ABC)

def_op('MODVV', 34, ARGS_ABC)

def_op('POW', 35, ARGS_ABC)

def_op('CAT', 36, ARGS_ABC)

def_op('KSTR', 37, ARGS_AD)

def_op('KCDATA', 38, ARGS_AD)

def_op('KSHORT', 39, ARGS_AD)

def_op('KNUM', 40, ARGS_AD)

def_op('KPRI', 41, ARGS_AD)

def_op('KNIL', 42, ARGS_AD)

def_op('UGET', 43, ARGS_AD)

def_op('USETV', 44, ARGS_AD)

def_op('USETS', 45, ARGS_AD)

def_op('USETN', 46, ARGS_AD)

def_op('USETP', 47, ARGS_AD)

def_op('UCLO', 48, ARGS_AD)

def_op('FNEW', 49, ARGS_AD)

def_op('TNEW', 50, ARGS_AD)

def_op('TDUP', 51, ARGS_AD)

def_op('GGET', 52, ARGS_AD)

def_op('GSET', 53, ARGS_AD)

def_op('TGETV', 54, ARGS_AD)

def_op('TGETS', 55, ARGS_AD)

def_op('TGETB', 56, ARGS_AD)

def_op('TSETV', 57, ARGS_AD)

def_op('TSETS', 58, ARGS_AD)

def_op('TSETB', 59, ARGS_AD)

def_op('TSETM', 60, ARGS_AD)

def_op('CALLM', 61, ARGS_ABC)

def_op('CALL', 62, ARGS_ABC)

def_op('CALLMT', 63, ARGS_AD)

def_op('CALLT', 64, ARGS_AD)

def_op('ITERC', 65, ARGS_ABC)

def_op('ITERN', 66, ARGS_ABC)

def_op('VARG', 67, ARGS_ABC)

def_op('ISNEXT', 68, ARGS_AD)

def_op('RETM', 69, ARGS_AD)

def_op('RET', 70, ARGS_AD)

def_op('RET0', 71, ARGS_AD)

def_op('RET1', 72, ARGS_AD)

def_op('FORI', 73, ARGS_AD)

def_op('JFORI', 74, ARGS_AD)

def_op('FORL', 75, ARGS_AD)

def_op('IFORL', 76, ARGS_AD)

def_op('JFORL', 77, ARGS_AD)

def_op('ITERL', 78, ARGS_AD)

def_op('IITERL', 79, ARGS_AD)

def_op('JITERL', 80, ARGS_AD)

def_op('LOOP', 81, ARGS_AD)

def_op('ILOOP', 82, ARGS_AD)

def_op('JLOOP', 83, ARGS_AD)

def_op('JMP', 84, ARGS_AD)

def_op('FUNCF', 85, ARGS_AD)

def_op('IFUNCF', 86, ARGS_AD)

def_op('JFUNCF', 87, ARGS_AD)

def_op('FUNCV', 88, ARGS_AD)

def_op('IFUNCV', 89, ARGS_AD)

def_op('JFUNCV', 90, ARGS_AD)

def_op('FUNCC', 91, ARGS_AD)

def_op('FUNCCW', 92, ARGS_AD)


unrolled_op_desc = unrolling_iterable(OP_DESC)
