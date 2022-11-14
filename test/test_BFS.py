import sys
import unittest
import pandas as pd

from pathlib import Path
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import DP
import BFS
# from RelationalOp import RelationalOp


import utils 

vis_attributes = ['user_id', 'public', 'completion_percentage', 'gender', 'last_login', 'age', 'body', 'I_am_working_in_field', 'spoken_languages', 'hobbies', 'region_large', 'region_small', 'height', 'weight']

missing = utils.load_missing()
df = pd.read_csv(parent+'/data/target_data.csv')

mgraph = utils.create_network(df, vis_attributes, 20000, missing)


class test_BFS(unittest.TestCase):

    def testPreBfs(self):
        appArgs = DP.parseArgs(['-t', 'region_large=Nitra Region', '-m', 'region_small=Nitra', '-b', 'age>=32'])
        arr = BFS.preBFS(mgraph, appArgs)
        self.assertEqual(arr[0][1], 14141)
        self.assertEqual(arr[0][0], 15494)
        self.assertEqual(arr[0][2], 6139)
        self.assertEqual(arr[0][3], 14889)
        self.assertEqual(arr[0][4], 15872)

if __name__ == '__main__':
	unittest.main()
