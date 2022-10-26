# Class to convert dictionary of input arguments into
# a more developer-friendly with member variables.
# AppArgs converts "key=value" in CLI to a dictionary of {'key': 'value'}

from Constraint import Constraint
from RelationalOp import RelationalOp

class AppArgs:
    # permitted constraint values (placeholder)
    TOP_CONSTRAINTS = {'top1', 'top2'}
    MED_CONSTRAINTS = {'med1', 'med2'}
    BOT_CONSTRAINTS = {'bot1', 'bot2', 'bot3'}

    def __init__(self, args: dict):
        self._args = args

    def verify(self):
        self._verifyHierarchy()
        self._convertArgsToHierarchy()
        self._checkValidKeys()

    # Verifies user passes arguments in a top down structure, ex:
    # top -> med -> bottom, or
    # top -> med, or
    # top
    def _verifyHierarchy(self):
        # remove all 'None' dict entries (which come from argparse)
        self._args = {key: val for key, val in self._args.items() if val is not None}

        # enforce top-down invariant
        if 'top' not in self._args:
            raise Exception('No top-level contraint found. Use -t <top_constraint=value>')
        elif 'bot' in self._args and 'med' not in self._args:
            raise Exception('No mid-level contraint found. Use -m <med_constraint=value>')

    def _convertArgsToHierarchy(self):
        self.top = self._convertArgsToMemberVariable('top')
        self.med = self._convertArgsToMemberVariable('med')
        self.bot = self._convertArgsToMemberVariable('bot')

    def _convertArgsToMemberVariable(self, key):
        if key not in self._args:
            return None # skip unspecified hierarchies

        # ex: convert 'k1=v1,k2=v2' into ['k1=v1', 'k2=v2']
        splitArgs = self._args[key].split(',')

        # ex: convert ['k1=v1', 'k2=v2'] into [['k1', 'v1'], ['k2', 'v2']]
        equalArgs = [x.split('=') for x in splitArgs]
        lengths = [len(x) for x in equalArgs]

        # check if any inputs were not in name=value syntax
        oddLengths = [x for x in lengths if x % 2]
        if len(oddLengths) > 0:
            raise Exception('Unexpected syntax. Use name=value')

        # check for empty values, ex: "name=" (no value)
        emptyValues = [x for x in equalArgs if len(x[1]) == 0]
        if len(emptyValues) > 0:
            raise Exception('Unexpected syntax. Use name=value where value is non-empty')

        # ex: convert [['k1', 'v1'], ['k2', 'v2']] into...
        #   [Constraint1('k1', 'v1', <relop>), Constraint2('k2', 'v2', <relop>)]
        constraints = []
        for elem in equalArgs:
            constraint = Constraint(elem[0], elem[1], RelationalOp.EQUAL)
            constraints.append(constraint)

        return constraints

    def _checkValidKeys(self):
        self._checkValidKey(self.top, self.TOP_CONSTRAINTS)
        self._checkValidKey(self.med, self.MED_CONSTRAINTS)
        self._checkValidKey(self.bot, self.BOT_CONSTRAINTS)

    # check if all user-specified keys equal permitted keys
    def _checkValidKey(self, member, permittedValues):
        if not member:
            return # nothing to check

        keys = set([x.key for x in member])
        if not keys.union(permittedValues) == permittedValues:
            sortedValues = sorted(list(permittedValues))
            raise Exception('Invalid keys found. Allowed keys are: ' + ' '.join(sortedValues))
