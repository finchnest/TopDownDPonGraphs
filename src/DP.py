from AppArgs import AppArgs
import argparse
import sys
import BFS

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
    
    constraint_qualifers = BFS.preBFS(appArgs)
    # print(BFS.BFS(BFS.mgraph, 1))
    
    population_count = constraint_qualifers[1]
    print(population_count)
    
    #noise addition function takes population count as an argument    
    

if __name__ == '__main__':
    main()
