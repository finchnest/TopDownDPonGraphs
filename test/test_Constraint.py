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


if __name__ == '__main__':
	unittest.main()
