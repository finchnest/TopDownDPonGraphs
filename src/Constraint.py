from RelationalOp import RelationalOp

class Constraint():
    def __init__(self, key: str, value: str, relationalOp: RelationalOp):
        self.key = key
        self.value = value
        self.relationalOp = relationalOp

    # ex argList: ['region_large<30', 'top2>=40']
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
