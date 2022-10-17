# Class to convert dictionary of input arguments into
# a more developer-friendly with member variables.
# AppArgs converts "key=value" in CLI to a dictionary of {'key': 'value'}

class AppArgs:
    # permitted constraint values (placeholder)
    TOP_CONSTRAINTS = {'top1', 'top2'}
    MED_CONSTRAINTS = {'med1', 'med2'}
    BOT_CONSTRAINTS = {'bot1', 'bot2', 'bot3'}

    def __init__(self, args: dict):
        self._args = args

    def verify(self):
        self._verifyHierarchy()
        self._convertDictToHierarchy()
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
            raise Exception('No top-level contraint found. Use -t <top_constraint>')
        elif 'bot' in self._args and 'med' not in self._args:
            raise Exception('No mid-level contraint found. Use -m <med_constraint>')

    def _convertDictToHierarchy(self):
        self.top = self._convertDictToMemberVariable('top')
        self.med = self._convertDictToMemberVariable('med')
        self.bot = self._convertDictToMemberVariable('bot')

    def _convertDictToMemberVariable(self, key):
        if key not in self._args:
            return None # skip unspecified hierarchies

        # ex: convert 'k1=v1,k2=v2' into ['k1=v1', 'k2=v2']
        splitArgs = self._args[key].split(',')

        # ex: convert ['k1=v1', 'k2=v2'] into [['k1', 'v1'], ['k2', 'v2']]
        equalArgs = [x.split('=') for x in splitArgs]

        # ex: convert [['k1', 'v1'], ['k2', 'v2']] into {'k1': 'v1', 'k2': 'v2'}
        dictArgs = dict(equalArgs)
        return dictArgs

    def _checkValidKeys(self):
        self._checkValidKey(self.top, self.TOP_CONSTRAINTS)
        self._checkValidKey(self.med, self.MED_CONSTRAINTS)
        self._checkValidKey(self.bot, self.BOT_CONSTRAINTS)

    # check if all user-specified keys equal permitted keys
    def _checkValidKey(self, member, permittedValues):
        if not member:
            return # nothing to check

        s = set(member.keys())
        if not s.union(permittedValues) == permittedValues:
            raise Exception('Invalid keys found. Allowed keys are: ' + ' '.join(s))
