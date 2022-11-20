from enum import Enum
import operator

class RelationalOp(Enum):
    LESS_THAN_EQ  = '<='
    GREAT_THAN_EQ = '>='
    EQUAL         = '='
    LESS_THAN     = '<'
    GREAT_THAN    = '>'
