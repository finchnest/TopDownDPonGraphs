import numpy as np
import sys
import unittest
import matplotlib.pyplot as plt

from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'src'))

from PostProcessing import PostProcessing

# Num rows for region_large="Zilina Region" and region_small="Kysucke New Town"
# with NO bottom constraints:
TOTAL_NUM_ROWS = 2187

class test_PostProcessing(unittest.TestCase):

    def testBasic(self):
        np.random.seed(seed=2) # need determinstic results to add tests

        count = 180
        sigma = 35
        muRange = [-3, 3]
        noisyCount = PostProcessing(count, sigma, TOTAL_NUM_ROWS, muRange)
        assert noisyCount == 175

    def testMaximumCount(self):
        np.random.seed(seed=1)

        muRange = [-3, 3]
        # create negative noisy count (which is maxed to zero)
        noisyCount = PostProcessing(TOTAL_NUM_ROWS, 10, TOTAL_NUM_ROWS, muRange)
        assert noisyCount == 2195

    def testMinimumCount(self):
        np.random.seed(seed=2)

        muRange = [-3, 3]
        # create negative noisy count (which is maxed to zero)
        noisyCount = PostProcessing(0, 10, TOTAL_NUM_ROWS, muRange)
        assert noisyCount == 0

    def testTotalError(self):
        np.random.seed(seed=3)

        # count and sigma from:
        # region_large="Zilina Region"
        # region_small="Kysucke New Town"
        # hobbies="music"
        count = 185
        sigma = 32.9

        muRange = [0, 0] # center around zero for first noise
        max = 200
        preProcessError = []
        noisyCounts = []
        for _ in range(0, max):
            # first noise addition
            noisyCount = PostProcessing(count, sigma, TOTAL_NUM_ROWS, muRange)
            preProcessError.append(abs(noisyCount - count))
            noisyCounts.append(noisyCount)

        totalPostProcessError = []
        mus = np.arange(.5, 10, .5)
        for mu in mus:
            muRange = [-mu, mu]
            postProcessError = []
            for i in range(0, max):
                # add 2nd round of noise using noisyCounts as starting point
                noisyCount = PostProcessing(noisyCounts[i], sigma, TOTAL_NUM_ROWS, muRange)
                postProcessError.append(abs(count - noisyCount))
            totalPostProcessError.append(sum(postProcessError))

        preProcessError = sum(preProcessError)
        assert preProcessError == 913
        assert sum(totalPostProcessError) == 29656

        # replicate value so that it can be plotted
        preProcessError = [preProcessError] * len(mus)

        plt.plot(mus, preProcessError, label='Pre-process error')
        plt.plot(mus, totalPostProcessError, label='Post-process error')
        plt.xlabel('Mu, note: value sampled between [-mu, mu]')
        plt.ylabel('Error magnitude')
        plt.legend()
        plt.title('Error vs Post-Processing Error For:\nregion="Zilina Region", town="Kysucke New Town", hobbies="music"')
        plt.savefig('PostProcessError.png')

if __name__ == '__main__':
	unittest.main()
