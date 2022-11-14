import sys
import unittest

# add 'src' folder to path to locate src classes
# TODO: is there a better way?
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'src'))

from Constraint import Constraint
from RelationalOp import RelationalOp

class test_Constraint(unittest.TestCase):

    def testEqual(self):
        c = Constraint('key', 'val', RelationalOp.EQUAL)
        self.assertEqual(c.key, 'key')
        self.assertEqual(c.value, 'val')
        self.assertEqual(c.relationalOp, RelationalOp.EQUAL)

    def testOther(self):
        c = Constraint('key', 'val', RelationalOp.LESS_THAN)
        self.assertEqual(c.relationalOp, RelationalOp.LESS_THAN)
        c = Constraint('key', 'val', RelationalOp.LESS_THAN_EQ)
        self.assertEqual(c.relationalOp, RelationalOp.LESS_THAN_EQ)
        c = Constraint('key', 'val', RelationalOp.GREAT_THAN)
        self.assertEqual(c.relationalOp, RelationalOp.GREAT_THAN)
        c = Constraint('key', 'val', RelationalOp.GREAT_THAN_EQ)
        self.assertEqual(c.relationalOp, RelationalOp.GREAT_THAN_EQ)

    def testRelationalOperators(self):
        # iterate over all supported relational operators:
        # =, <, <=, >, >=
        self.assertEqual(len(RelationalOp), 5)

        for relop in RelationalOp:
            with self.subTest():
                s = ['region_large' + relop.value[0] + '10']
                constraints = Constraint.convertArgsToConstraints(s)
                self.assertEqual(len(constraints), 1)
                constraint = constraints[0]
                self.assertEqual(constraint.key, 'region_large')
                self.assertEqual(constraint.value, '10')
                self.assertEqual(constraint.relationalOp, relop)

if __name__ == '__main__':
	unittest.main()
