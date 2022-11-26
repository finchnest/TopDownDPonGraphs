from AppArgs import AppArgs
import argparse
import sys
import pandas as pd
import numpy as np
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import GlobalSens
import utils
import noise
import matplotlib.pyplot as plt
import BFS

vis_attributes = ['gender', 'region_large', 'region_small', 'age', 'weight', 'height', 'hobbies', 'user_id']

missing = utils.load_missing()
df = pd.read_csv(parent+'/data/anonymized_data.csv')

mgraph = utils.create_network(df, vis_attributes, 20000, missing)

# verify input arguments using argparse and AppArgs
def parseArgs(args):
    parser = argparse.ArgumentParser()

    parser.add_argument('-t', '--top', metavar='TOP', type=str,
                        help='Top level constraint')
    parser.add_argument('-m', '--med', metavar='MEDIUM',
                        help='Medium level constraint')
    parser.add_argument('-b', '--bot', metavar='BOTTOM',
                        help='Bottom level constraint')

    args = vars(parser.parse_args(args))

    # verify args
    appArgs = AppArgs(args)
    appArgs.verify()

    return appArgs

def main():
    # forward command line arguments to be validated (sys.argv)
    appArgs = parseArgs(sys.argv[1:])

    # debug purposes (delete when no longer necessary)
    # print(appArgs)
    # print(appArgs.top)
    # print(appArgs.med)
    # print(appArgs.bot)

    # forward command line arguments to the BFS search function

    #value updated after a node removal

    # updated above

    # constraint_qualifers = BFS.preBFS(mgraph, appArgs)
    # population_count = constraint_qualifers[1]
    noisy_val = []
    val = []
    #  global sensitivity
    gs = GlobalSens.compute_global_sens('../data/target_data.csv', 'l1', appArgs)
    epsilons = [i for i in np.arange(0.01, 1.01, 0.1)]
    # epsilon should not be 0
    assert not any(e == 0 for e in epsilons)

    for e in epsilons:
        assert e != 0.0
        sigma = (2*np.log(1.25/1)*(gs**2))/(e**2)
        true_q = BFS.BFS(mgraph, appArgs)[0]
        val.append(true_q)

        n = 0
        for _ in range(10):
            n += abs(noise.sample_dgauss(sigma))

        noisy_val.append(n/10)

    plt.plot(epsilons, noisy_val)
    plt.title('Tradeoff between privacy and error')
    plt.xlabel('epsilon')
    plt.ylabel('error')
    plt.savefig('./errors.png')

    # # define histograms, have to manually change plot title and file name
    # fig, ax = plt.subplots(figsize=(12, 8))
    # bar_width = 0.4
    # x = np.arange(10)
    # b1 = ax.bar(x, val, width=bar_width, label='true value')
    # b2 = ax.bar(x + bar_width, noisy_val, label = 'noisy value', width=bar_width)
    # ax.set_xticks(x + bar_width / 2)
    # ax.set_xticklabels([0.01, 0.11, 0.21, 0.31, 0.41, 0.51, 0.61, 0.71, 0.81, 0.91])
    # ax.legend()
    # ax.set_title(f'Comparision on hobby=music', pad=15)
    # plt.savefig('Noisy_hobby_count.png')

    # Please try: python DP.py -t region_large="Zilina Region" -m region_small="Kysucke New Town" -b hobbies="music"

    # return population_count

    #  result_x  = noise_add_func(population_count)

    #fidelity check

    # return to user

    #noise addition function takes population count as an argument


if __name__ == '__main__':
    main()
