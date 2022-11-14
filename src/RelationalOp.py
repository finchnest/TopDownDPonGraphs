from enum import Enum
import operator

class RelationalOp(Enum):
    LESS_THAN_EQ  = ['<=', operator.le]
    GREAT_THAN_EQ = ['>=', operator.ge]
    EQUAL         = ['=', operator.eq]
    LESS_THAN     = ['<', operator.lt]
    GREAT_THAN    = ['>', operator.gt]
