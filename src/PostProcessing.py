import math
import numpy as np

def PostProcessing(count, sigma, maxPossibleCount, muRange):
    assert len(muRange) == 2
    assert muRange[0] <= muRange[1]

    # Create linear equation which weights high mu for high counts
    # and low (negative) mu for low counts.
    # This is an attempt to simplify and reproduce Top-Down's privacy
    # budget which found that their Top-Down algorithm inherently
    # "moved" people from large population centers to small

    # slope = (y2 - y1)/(x2 - x1)
    slope = (muRange[1] - muRange[0]) / (maxPossibleCount - 0)

    # mu = slope*x + b (b = y-intercept = minimum mu value)
    mu = slope * count + muRange[0]

    # sample noise using adjusted mu
    noise = np.random.normal(mu, math.sqrt(sigma))
    noisyCount = count + round(noise)

    # ensure positive value
    noisyCount = max(noisyCount, 0)
    return noisyCount
