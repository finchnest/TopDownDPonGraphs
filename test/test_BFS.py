import sys
import unittest
import pandas as pd

from pathlib import Path
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'src'))

import DP
from BFS import BFS
import utils

vis_attributes = ['user_id', 'public', 'completion_percentage', 'gender', 'last_login',
                  'age', 'body', 'I_am_working_in_field', 'spoken_languages', 'hobbies',
                  'region_large', 'region_small', 'height', 'weight']

missing = utils.load_missing()
df = pd.read_csv(parent+'/data/target_data.csv')

mgraph = utils.create_network(df, vis_attributes, 20000, missing)


class test_BFS(unittest.TestCase):

    def testBfs(self):
        appArgs = DP.parseArgs(['-t', 'region_large=Nitra Region', '-m', 'region_small=Nitra',
                                '-b', 'age>=32'])
        arr = BFS(mgraph, appArgs)
        self.assertEqual(len(arr), 5)
        self.assertEqual(arr[0], 15494)
        self.assertEqual(arr[1], 14141)
        self.assertEqual(arr[2], 6139)
        self.assertEqual(arr[3], 14889)
        self.assertEqual(arr[4], 15872)

    def testBfsMultipleBottomConstraints(self):
        appArgs = DP.parseArgs(['-t', 'region_large=abroad', '-m', 'region_small=abroad - others',
                                '-b', 'age>35,gender=1'])
        arr = BFS(mgraph, appArgs)
        self.assertEqual(len(arr), 4)
        self.assertEqual(arr[0], 3734)
        self.assertEqual(arr[1], 7204)
        self.assertEqual(arr[2], 19815)
        self.assertEqual(arr[3], 13875)

    def testHobbies(self):
        appArgs = DP.parseArgs(['-t', 'region_large=Zilina Region', '-m', 'region_small=Kysucke New Town',
                                '-b', 'hobbies=technology'])
        arr = BFS(mgraph, appArgs)
        self.assertEqual(len(arr), 2)
        self.assertEqual(arr[0], 53)
        self.assertEqual(arr[1], 16534)

    def testHeight(self):
        appArgs = DP.parseArgs(['-t', 'region_large=Zilina Region', '-m', 'region_small=Kysucke New Town',
                                '-b', 'height>202'])
        arr = BFS(mgraph, appArgs)
        self.assertEqual(len(arr), 6)
        self.assertEqual(arr[0], 636)
        self.assertEqual(arr[1], 2982)
        self.assertEqual(arr[2], 3353)
        self.assertEqual(arr[3], 2314)
        self.assertEqual(arr[4], 18911)
        self.assertEqual(arr[5], 15091)

    def testEmptySubstring(self):
        appArgs = DP.parseArgs(['-t', 'region_large=Zil', '-m', 'region_small=Zil'])
        arr = BFS(mgraph, appArgs)
        self.assertEqual(len(arr), 0)

    def testAgeRange(self):
        appArgs = DP.parseArgs(['-t', 'region_large=Zilina Region', '-m', 'region_small=Kysucke New Town',
                                '-b', 'age>=46,age<=47'])
        arr = BFS(mgraph, appArgs)
        self.assertEqual(len(arr), 2)
        self.assertEqual(arr[0], 2191)
        self.assertEqual(arr[1], 15936)

    def testWeight(self):
        appArgs = DP.parseArgs(['-t', 'region_large=Zilina Region', '-m', 'region_small=Kysucke New Town',
                                '-b', 'weight>=99,age>35'])
        arr = BFS(mgraph, appArgs)
        self.assertEqual(len(arr), 3)
        self.assertEqual(arr[0], 4694)
        self.assertEqual(arr[1], 17617)
        self.assertEqual(arr[2], 15091)

if __name__ == '__main__':
	unittest.main()
