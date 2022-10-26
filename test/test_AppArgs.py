import sys
import unittest

# add 'src' folder to path to locate src classes
# TODO: is there a better way?
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'src'))

from AppArgs import AppArgs
from Constraint import Constraint
from RelationalOp import RelationalOp

class test_AppArgs(unittest.TestCase):

    def testBasic(self):
        args = {'top': 'top2=1',
                'med': 'med2=2',
                'bot': 'bot1=3'}
        appArgs = AppArgs(args)
        appArgs.verify()
        self.assertIsInstance(appArgs.top, list)
        self.assertIsInstance(appArgs.top[0], Constraint)
        self.assertIsInstance(appArgs.med, list)
        self.assertIsInstance(appArgs.med[0], Constraint)
        self.assertIsInstance(appArgs.bot, list)
        self.assertIsInstance(appArgs.bot[0], Constraint)

    def testArgSplit(self):
        args = {'top': 'top1=abc,top2=25'}
        appArgs = AppArgs(args)
        appArgs.verify()
        self.assertEqual(len(appArgs.top), 2)
        self.assertEqual(appArgs.top[0].key, 'top1')
        self.assertEqual(appArgs.top[0].value, 'abc')
        self.assertEqual(appArgs.top[1].key, 'top2')
        self.assertEqual(appArgs.top[1].value, '25')

    def testArgSplitHierarchy(self):
        args = {'top': 'top1=t1,top2=10',
                'med': 'med1=m1',
                'bot': 'bot1=b1,bot2=b2'}
        appArgs = AppArgs(args)
        appArgs.verify()
        self.assertEqual(len(appArgs.top), 2)
        self.assertEqual(appArgs.top[0].key, 'top1')
        self.assertEqual(appArgs.top[0].value, 't1')
        self.assertEqual(appArgs.top[0].relationalOp, RelationalOp.EQUAL)
        self.assertEqual(appArgs.top[1].key, 'top2')
        self.assertEqual(appArgs.top[1].value, '10')
        self.assertEqual(appArgs.top[1].relationalOp, RelationalOp.EQUAL)

        self.assertEqual(len(appArgs.med), 1)
        self.assertEqual(appArgs.med[0].key, 'med1')
        self.assertEqual(appArgs.med[0].value, 'm1')
        self.assertEqual(appArgs.med[0].relationalOp, RelationalOp.EQUAL)

        self.assertEqual(len(appArgs.bot), 2)
        self.assertEqual(appArgs.bot[0].key, 'bot1')
        self.assertEqual(appArgs.bot[0].value, 'b1')
        self.assertEqual(appArgs.bot[0].relationalOp, RelationalOp.EQUAL)
        self.assertEqual(appArgs.bot[1].key, 'bot2')
        self.assertEqual(appArgs.bot[1].value, 'b2')
        self.assertEqual(appArgs.bot[1].relationalOp, RelationalOp.EQUAL)

    def testTopInvalidValue(self):
        args = {'top': 'fake=f'}
        appArgs = AppArgs(args)

        try:
            appArgs.verify()
        except Exception as ex:
            self.assertNotIn('fake', ex.args[0])
            self.assertIn('top1 top2', ex.args[0])
            return

        self.assertTrue(False, 'Test should throw exception')

    def testMedInvalidValue(self):
        args = {'top': 'top1=t', 'med': 'fake=f'}
        appArgs = AppArgs(args)
        self.assertRaises(Exception, lambda: appArgs.verify())

    def testBotInvalidValue(self):
        args = {'top': 'top1=t', 'med': 'med1=1', 'bot': 'fake=f'}
        appArgs = AppArgs(args)
        self.assertRaises(Exception, lambda: appArgs.verify())

    # CLI not in form of name=value
    def testNoEqualSign(self):
        args = {'top': 'top1'} # 'top1' instead of 'top1=value'
        appArgs = AppArgs(args)

        try:
            appArgs.verify()
        except Exception as ex:
            self.assertNotIsInstance(ex, ValueError)
            self.assertIsInstance(ex, Exception)
            return

        self.assertTrue(False, 'Test should throw exception')

    # Form of "name=" with no value
    def testEmptyValue(self):
        args = {'top': 'top1='}
        appArgs = AppArgs(args)
        self.assertRaises(Exception, lambda: appArgs.verify())

if __name__ == '__main__':
	unittest.main()
