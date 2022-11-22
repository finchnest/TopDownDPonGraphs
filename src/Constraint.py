from RelationalOp import RelationalOp
import operator
import re

class Constraint():
    # permitted constraint values
    TOP_CONSTRAINTS = {'region_large', 'top2'}
    MED_CONSTRAINTS = {'region_small', 'med2'}
    BOT_CONSTRAINTS = {'age', 'gender', 'hobbies', 'height', 'weight'} # todo: add more here

    def __init__(self, key: str, value: str, relationalOp: RelationalOp):
        self.key = key
        self.value = value
        self.relationalOp = relationalOp
        self.opFcn = Constraint._getOperatorFunction(relationalOp)
        if self.key in Constraint.BOT_CONSTRAINTS:
            self.castFcn = self._getCastFunction()

    # return operator to do criteria
    # ex: for char '<=', this returns operator.le
    @staticmethod
    def _getOperatorFunction(relationalOp):
        if relationalOp == RelationalOp.LESS_THAN_EQ:
            opFcn = operator.le
        elif relationalOp == RelationalOp.GREAT_THAN_EQ:
            opFcn = operator.ge
        elif relationalOp == RelationalOp.EQUAL:
            opFcn = operator.eq
        elif relationalOp == RelationalOp.LESS_THAN:
            opFcn = operator.lt
        else:
            assert relationalOp == RelationalOp.GREAT_THAN
            opFcn = operator.gt

        return opFcn

    def _getCastFunction(self):
        assert self.key in Constraint.BOT_CONSTRAINTS

        # todo: add other bottom args here
        # if self.key in ['age', 'gender']:
        if self.key in ['gender']: # putting age into str
            castFcn = int
        elif self.key in ['height', 'weight']:
            # ex: convert '175 cm' to 175 (int)
            # or '90 kg' to 90 (int)
            castFcn = lambda x : int(re.findall(r'\d+', x)[0])
        else:
            castFcn = str
            # use contains operator to match substrings:
            self.opFcn = operator.contains

        return castFcn

    # ex input: ['region_large<30', 'top2>=40']
    # ex output: [Constraint('region_large', '30', <), Constraint('top2', '40', >=)]
    @staticmethod
    def convertArgsToConstraints(argList: list):
        constraints = []
        for arg in argList:

            for relop in RelationalOp:
                if relop.value in arg:
                    relopType = relop
                    break

            splitArgs = arg.split(relopType.value)

            # check if any inputs were not in name=value syntax
            if len(splitArgs) % 2 > 0:
                raise Exception('Unexpected syntax. Use name=value')

            # check for empty values, ex: "name=" (no value)
            emptyValues = [x for x in splitArgs if len(x) == 0]
            if len(emptyValues) > 0:
               raise Exception('Unexpected syntax. Use name=value where value is non-empty')

            constraint = Constraint(splitArgs[0], splitArgs[1], relopType)
            constraints.append(constraint)

        return constraints
