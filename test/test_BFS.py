import sys
import unittest

from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'src'))

import DP
import BFS
# from RelationalOp import RelationalOp

class test_BFS(unittest.TestCase):

    def testPreBfs(self):
        appArgs = DP.parseArgs(['-t', 'region_large=Nitra Region', -m, 'region=small=Zilina', -b, 'age>=32'])
        arr = BFS.preBFS(appArgs)
        self.assertEqual(arr[0], 3)
        self.assertEqual(arr[1], 6)
        self.assertEqual(arr[2], 36)

if __name__ == '__main__':
	unittest.main()
