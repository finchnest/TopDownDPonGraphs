from platform import node
from turtle import clear
import pandas as pd
import sys
import os
import random
from RelationalOp import RelationalOp
import copy



# import os 
# dir_path = os.path.dirname(os.path.realpath(__file__)) #src
# from pathlib import Path
# parent_folder = Path(dir_path).parent.absolute() #Top...

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

# print(parent)

import utils 

vis_attributes = ['user_id', 'public', 'completion_percentage', 'gender', 'region', 'last_login', 'registration', 'AGE', 'body', 'I_am_working_in_field', 'spoken_languages', 'hobbies']

missing = utils.load_missing()
df = pd.read_csv('../toy_example_500.csv')
mgraph = utils.create_network(df, vis_attributes, 50, missing)

neighbor_info = utils.get_neighbor_information() 

size = 50

def preBFS(appArgs):

    return BFS(mgraph, mgraph.nodes[1]['user_id'], appArgs)

def BFS(graph, source_node, constraints):

    # Mark all the vertices as not visited
    visited = [False] * (size)
    queue = []
    # Mark the source node as
    # visited and enqueue it
    queue.append(source_node)
    visited[source_node - 1] = True
    result = []
    while queue:

        current = queue.pop(0)
        
        # We know at least the top constraint is always defined so only check medium and bottom.
        # The if check below is a placeholder for now until we finalize decision on constraint structure.
        if(constraints):
            # top_key = constraints.top[0].key
            top_key = 'AGE'#for testing since there's no attribute called top1
            top_value = constraints.top[0].value
            top_ops = constraints.top[0].relationalOp

            if(top_ops == RelationalOp.EQUAL):
                if (graph.nodes[current][top_key] == int(top_value)):
                    result.append(current)

            elif (top_ops == RelationalOp.GREAT_THAN):
                if (graph.nodes[current][top_key] > int(top_value)):
                    result.append(current)

            elif (top_ops == RelationalOp.LESS_THAN):
                if (graph.nodes[current][top_key] < int(top_value)):
                    result.append(current)

            elif (top_ops == RelationalOp.LESS_THAN_EQ):
                if (graph.nodes[current][top_key] <= int(top_value)):
                    result.append(current)

            else:
                if (graph.nodes[current][top_key] >= int(top_value)):
                    result.append(current)


        # Get all adjacent vertices of the
        # dequeued vertex.
        for i in neighbor_info[current]:
            if visited[i - 1] == False:
                queue.append(i)
                visited[i - 1] = True 
    return result

# top_constraint_qualifers = BFS(mgraph, mgraph.nodes[1]['user_id'], constraint_dict=top)
