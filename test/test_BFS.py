import sys
import unittest

from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'src'))

import DP
import BFS
# from RelationalOp import RelationalOp

class test_BFS(unittest.TestCase):

    def testPreBfs(self):
        appArgs = DP.parseArgs(['-t', 'region_large=Nitra Region', '-m', 'region_small=Nitra', '-b', 'age>=32'])
        arr = BFS.preBFS(appArgs)
        self.assertEqual(arr[0][0], 14141)
        self.assertEqual(arr[0][1], 15494)
        self.assertEqual(arr[0][2], 6139)
        self.assertEqual(arr[0][3], 14889)
        self.assertEqual(arr[0][4], 15872)

if __name__ == '__main__':
	unittest.main()
