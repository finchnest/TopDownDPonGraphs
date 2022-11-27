from AppArgs import AppArgs
import argparse
import sys
import pandas as pd
import numpy as np
import os
import cdp2adp
from fractions import Fraction

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import GlobalSens
import utils
import noise
import matplotlib.pyplot as plt
import BFS
import seaborn as sn

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


    #  global sensitivity
    gs = GlobalSens.compute_global_sens('../data/target_data.csv', 'l1', appArgs)
    epsilons = [i for i in np.arange(0.0001, 1.0001, 0.05)]
    # epsilon should not be 0
    assert not any(e == 0 for e in epsilons)

    total_queries = [i for i in range(1, 11)] # this denotes how many queries a user want at a time, and the privacy budget will be distributed to these queries

    noisy_queries = []
    for k in total_queries:

        # updated above
        noisy_val = []
        val = []

        for e in epsilons:
            assert e != 0.0

            delta=0.1
            #convert to concentrated DP
            rho=cdp2adp.cdp_rho(e,delta)
            rho_per_q = Fraction(rho)/k 
            sigma=1/(2*rho_per_q)
            #actual variance, at most sigma2
            print(str(round(rho, 6))+"-CDP implies ("+str(round(e, 2))+","+str(delta)+")-DP ||", f"True DP coefficient: Epsilon={round(e, 2)} | Budget={round(delta/k, 3)} | Sigma={sigma}")
            # USE this code below if u want to queries other than count

            n = 0
            for _ in range(10):
                n += abs(noise.sample_dgauss(sigma))

            noisy_val.append(n/10)

        noisy_queries.append(noisy_val)

    sn.set(font_scale=0.7)
    epsilons = [round(e, 3) for e in epsilons]
    total_queries = [i for i in range(10, 0, -1)]
    sn.heatmap(noisy_queries, xticklabels=epsilons, yticklabels=total_queries, annot=True)
    plt.title('Error And QueryAmount Relationship(delta=0.1)')
    plt.xlabel('Epsilon')
    plt.ylabel('Queries Amount')
    plt.savefig('ErrorHeatMap.png')

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
