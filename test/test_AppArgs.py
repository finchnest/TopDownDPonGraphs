# Note: to run all tests:
# > python -m unittest

# This syntax requires a folder to be called 'test' and test file names prefixed with 'test_'

import sys
import unittest

# add 'src' folder to path to locate src classes
# TODO: is there a better way?
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'src'))

from AppArgs import AppArgs

class tAppArgs(unittest.TestCase):

    def testBasic(self):
        args = {'top': 'top2=1',
                'med': 'med2=2',
                'bot': 'bot1=3'}
        appArgs = AppArgs(args)
        appArgs.verify()
        self.assertIsInstance(appArgs.top, dict)
        self.assertIsInstance(appArgs.med, dict)
        self.assertIsInstance(appArgs.bot, dict)

    def testArgSplit(self):
        args = {'top': 'top1=abc,top2=25'}
        appArgs = AppArgs(args)
        appArgs.verify()
        self.assertEqual(appArgs.top['top1'], 'abc')
        self.assertEqual(appArgs.top['top2'], '25')

    def testArgSplitHierarchy(self):
        args = {'top': 'top1=t1,top2=10',
                'med': 'med1=m1',
                'bot': 'bot1=b1,bot2=b2'}
        appArgs = AppArgs(args)
        appArgs.verify()
        self.assertEqual(appArgs.top, {'top1': 't1', 'top2': '10'})
        self.assertEqual(appArgs.med, {'med1': 'm1'})
        self.assertEqual(appArgs.bot, {'bot1': 'b1', 'bot2': 'b2'})

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
