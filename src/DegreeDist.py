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

import seaborn as sns
from collections import Counter


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
    noisy_val = []
    val = []
    #  global sensitivity
    gs = GlobalSens.compute_global_sens('../data/target_data.csv', 'l1', appArgs)
    epsilons = [i for i in np.arange(0.01, 1.01, 0.1)]
    # epsilon should not be 0
    assert not any(e == 0 for e in epsilons)


    #degree distribution
    epi = 0.5
    edge_df = pd.read_csv(parent+'/data/example_edge_20k.csv')
    neighbor_info = utils.get_neighbor_information(edge_df)
    true_q = BFS.BFS(mgraph, appArgs)

    print('people amount', len(true_q))
    edge_counts = []

    for node_id in true_q:
        edge_count = len(neighbor_info[node_id])
        edge_counts.append(edge_count)

    hist = Counter(edge_counts)

    noisy_data ={}
    delta=0.9
    rho=cdp2adp.cdp_rho(epi,delta)
    k=len(hist)
    rho_per_q = Fraction(rho)/k 
    sigma=1/(2*rho_per_q)

    max_v, min_v = max(list(hist.keys())), min(list(hist.keys()))
    sample_range = [max(list(hist.values())), min(list(hist.values()))]

    print('max min degree', max_v, min_v)
    for i in range(min_v, max_v+1):
        if i in hist.keys():
            noisy_value = hist[i] + noise.sample_dgauss(sigma)
            noisy_data[i] = noisy_value

    true_query = []
    for k, v in hist.items(): 
        for _ in range(v):
            true_query.append(k)

    noisy_query = []
    for k, v in noisy_data.items(): 
        for _ in range(v):
            noisy_query.append(k)

    print('noise', len(noisy_query))
    print('true', len(true_query))

    # sns.histplot([true_query, noisy_query], label = ['true value', 'noisy value'],  kde=[True, True])
    # plt.hist(x=true_query, label = 'true value', color='darkorange', bins=40, alpha=0.5)
    # plt.hist(x=noisy_query, label =  'noisy value', color='cornflowerblue', bins=40, alpha=0.5)

    fig, ax = plt.subplots()
    for i, a in enumerate([true_query, noisy_query]):
        if i == 0:
            sns.histplot(a, ax=ax, kde=True, alpha=0.5, color='darkorange', bins=40, legend=True, label='true',binwidth=3, stat='percent')
        else:
            sns.histplot(a, ax=ax, kde=True, alpha=0.5, color='cornflowerblue', bins=40, legend=True, label='noisy', binwidth=3, stat='percent')

    plt.legend()
    plt.xlabel('Degree')
    plt.ylabel('Counts')
    plt.title('Cumulative Degree Distribution')
    plt.savefig('DegreeDist.png')


if __name__ == '__main__':
    main()
