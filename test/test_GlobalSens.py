import sys
import unittest

from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'src'))

import DP
import GlobalSens

class test_BFS(unittest.TestCase):

    def testGs1(self):
        appArgs = DP.parseArgs(['-t', 'region_large=Nitra Region', '-m', 'region_small=Nitra',
                                '-b', 'age>20'])
        gs = GlobalSens.compute_global_sens('data/target_data.csv', 'l1', appArgs)
        assert gs == 1

    def testGs0(self):
        appArgs = DP.parseArgs(['-t', 'region_large=Nitra Region', '-m', 'region_small=Nitra',
                                '-b', 'hobbies=<fake_data>'])
        gs = GlobalSens.compute_global_sens('data/target_data.csv', 'l1', appArgs)
        assert gs == 0

if __name__ == '__main__':
	unittest.main()
