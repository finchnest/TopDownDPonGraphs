import sys
import unittest

# add 'src' folder to path to locate 'DP'
# TODO: is there a better way?
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'src'))

import DP
from RelationalOp import RelationalOp

class test_CommandLineInterface(unittest.TestCase):

    # short form: -t, -m, -b
    def testShortForm(self):
        appArgs = DP.parseArgs(['-t', 'region_large=constraint1', '-m', 'med2=constraint2', '-b', 'bot3=constraint3'])
        self.assertEqual(appArgs.top[0].key, 'region_large')
        self.assertEqual(appArgs.top[0].value, 'constraint1')
        self.assertEqual(appArgs.med[0].key, 'med2')
        self.assertEqual(appArgs.med[0].value, 'constraint2')
        self.assertEqual(appArgs.bot[0].key, 'bot3')
        self.assertEqual(appArgs.bot[0].value, 'constraint3')

    # long form: --top, --med, --bottom
    def testLongForm(self):
        appArgs = DP.parseArgs(['--top', 'region_large=constraint1', '--med', 'med2=constraint2', '--bot', 'bot3=constraint3'])
        self.assertEqual(appArgs.top[0].key, 'region_large')
        self.assertEqual(appArgs.top[0].value, 'constraint1')
        self.assertEqual(appArgs.med[0].key, 'med2')
        self.assertEqual(appArgs.med[0].value, 'constraint2')
        self.assertEqual(appArgs.bot[0].key, 'bot3')
        self.assertEqual(appArgs.bot[0].value, 'constraint3')

    # ex: DP.py -t t -m name,age
    def testCommaSeparatedValues(self):
        appArgs = DP.parseArgs(['-t', 'region_large=t1', '-m', 'region_small=m1,med2=m2'])
        self.assertEqual(appArgs.top[0].key, 'region_large')
        self.assertEqual(appArgs.top[0].value, 't1')

        self.assertEqual(len(appArgs.med), 2)
        self.assertEqual(appArgs.med[0].key, 'region_small')
        self.assertEqual(appArgs.med[0].value, 'm1')
        self.assertEqual(appArgs.med[1].key, 'med2')
        self.assertEqual(appArgs.med[1].value, 'm2')

    def testIncorrectHierarchy(self):
        # no args
        self.assertRaises(Exception, DP.parseArgs, [])
        # medium constraint without top
        self.assertRaises(Exception, DP.parseArgs, ['-m', 'region_small=m'])
        # bottom constraint without top
        self.assertRaises(Exception, DP.parseArgs, ['-b', 'age=b'])
        # medium and bottom constraint without top
        self.assertRaises(Exception, DP.parseArgs, ['-m', 'region_small=m', '-b', 'age=b'])
        # top and bottom, but no medium
        self.assertRaises(Exception, DP.parseArgs, ['-t', 'region_large=t', '-b', 'age=b'])

    def testRelationalOperators(self):
        appArgs = DP.parseArgs(['-t', 'region_large>t1', '-m', 'region_small<=m1,med2>=m2', '-b', 'age<b3'])
        self.assertEqual(appArgs.top[0].key, 'region_large')
        self.assertEqual(appArgs.top[0].value, 't1')
        self.assertEqual(appArgs.top[0].relationalOp, RelationalOp.GREAT_THAN)

        self.assertEqual(appArgs.med[0].key, 'region_small')
        self.assertEqual(appArgs.med[0].value, 'm1')
        self.assertEqual(appArgs.med[0].relationalOp, RelationalOp.LESS_THAN_EQ)

        self.assertEqual(appArgs.med[1].key, 'med2')
        self.assertEqual(appArgs.med[1].value, 'm2')
        self.assertEqual(appArgs.med[1].relationalOp, RelationalOp.GREAT_THAN_EQ)

        self.assertEqual(appArgs.bot[0].key, 'age')
        self.assertEqual(appArgs.bot[0].value, 'b3')
        self.assertEqual(appArgs.bot[0].relationalOp, RelationalOp.LESS_THAN)

if __name__ == '__main__':
	unittest.main()
