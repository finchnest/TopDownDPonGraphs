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


vis_attributes = ['user_id', 'public', 'completion_percentage', 'gender', 'last_login',
                  'age', 'body', 'I_am_working_in_field', 'spoken_languages', 'hobbies',
                  'region_large', 'region_small', 'height', 'weight']

missing = utils.load_missing()
df = pd.read_csv(parent+'/data/target_data.csv')


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
    gs = GlobalSens.compute_global_sens('l1', appArgs)
    dif = []
    epsilons = [i for i in range(0, 5, 0.1)]
    
    for e in epsilons:
        n = 0
        for _ in range(5):
            sigma = (2*np.log(1.25/1))/(e**2)
            q = BFS.BFS(mgraph, appArgs)[0]
            n += noise.sample_dgauss(sigma)
        n = n / 5
        dif.append(n)

    plt.plot(epsilons, n)
    plt.show()
    plt.savefig('epsilons.png')

    # return population_count

    #  result_x  = noise_add_func(population_count)

    #fidelity check

    # return to user

    #noise addition function takes population count as an argument


if __name__ == '__main__':
    main()
