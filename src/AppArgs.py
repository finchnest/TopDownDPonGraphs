# Class to convert dictionary of input arguments into
# a more developer-friendly with member variables.
# AppArgs converts "key=value" in CLI to a dictionary of {'key': 'value'}

from Constraint import Constraint

class AppArgs:
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

        return Constraint.convertArgsToConstraints(splitArgs)

    def _checkValidKeys(self):
        self._checkValidKey(self.top, Constraint.TOP_CONSTRAINTS)
        self._checkValidKey(self.med, Constraint.MED_CONSTRAINTS)
        self._checkValidKey(self.bot, Constraint.BOT_CONSTRAINTS)

    # check if all user-specified keys equal permitted keys
    def _checkValidKey(self, member, permittedValues):
        if not member:
            return # nothing to check

        keys = {x.key for x in member}
        if not keys.union(permittedValues) == permittedValues:
            sortedValues = sorted(list(permittedValues))
            raise Exception('Invalid keys found. Allowed keys are: ' + ' '.join(sortedValues))
