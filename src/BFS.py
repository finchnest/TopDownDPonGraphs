from platform import node
from turtle import clear
import pandas as pd
import sys
import os
import random
import copy

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import utils

vis_attributes = ['user_id', 'public', 'completion_percentage', 'gender', 'region', 'last_login', 'registration', 'AGE', 'body', 'I_am_working_in_field', 'spoken_languages', 'hobbies']

missing = utils.load_missing()
df = pd.read_csv('../toy_example_500.csv')
mgraph = utils.create_network(df, vis_attributes, 50, missing)

neighbor_info = utils.get_neighbor_information() 

#test constrains
top = {'public': '1'}
med = {'gender': '0'}
bot = {'bot1': '180', 'gender':'male'}

def BFS(graph, source_node, constraint_dict, size=50):

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
        if( 'public' in constraint_dict.keys()):
   
            if (graph.nodes[current]['public'] == int(constraint_dict['public'])):
                result.append(current)

        # Get all adjacent vertices of the
        # dequeued vertex.
        for i in neighbor_info[current]:
            if visited[i - 1] == False:
                queue.append(i)
                visited[i - 1] = True 
    return result

top_constraint_qualifers = BFS(mgraph, mgraph.nodes[1]['user_id'], constraint_dict=top)
print(top_constraint_qualifers)

