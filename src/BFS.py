import pandas as pd
from collections import defaultdict

import sys
import os

current = os.path.dirname(os.path.realpath(__file__))

parent = os.path.dirname(current)

sys.path.append(parent)

import utils

vis_attributes = ['user_id', 'public', 'completion_percentage', 'gender', 'region', 'last_login', 'registration', 'AGE', 'body', 'I_am_working_in_field', 'spoken_languages', 'hobbies']

missing = utils.load_missing()
df = pd.read_csv('../toy_example_500.csv')
mgraph = utils.create_network(df, vis_attributes, 50, missing)

# print(len(net.nodes)) # node id
# print(net.nodes[1])
# print(net.nodes[5]['region'])


neighbor_info = utils.get_neighbor_information() 
# print(neighbor_info)

# this is a dict like {node_idx: [neighbor_1, neighbor_2 ,...]}
# Let's say you want the indices of neighbors with node No.5:

# neighbors = neighbor_info[33]
# print(neighbors)
# this will return a list with all neighbor indices

# subgraph = net.subgraph([1,2, 3])
# print(len(subgraph))
# print(subgraph.nodes)
# print(subgraph.nodes[1]['user_id'])
# print(type(net))
# print(subgraph.nodes[1]['region'])

# for node in subgraph:
#     print(node)
#     print('\n')
#     print(subgraph.nodes[node])

# for node in neighbor_info[33]:
#     print(node)
 
# Function to print a BFS of graph

# constraint = {
#     'top': 28,
#     'med': 1
# }

#example case: top level constraint => age>=28 and medium level constraint => gender == 1

def BFS(graph, source_node, constraint, size=50):

    # Mark all the vertices as not visited
    visited = [False] * (size)

    # Create a queue for BFS
    queue = []

    # Mark the source node as
    # visited and enqueue it
    queue.append(source_node)
    visited[source_node - 1] = True

    result = []

    while queue:

        # Dequeue a vertex from
        # queue and print it
        current = queue.pop(0)
        # print (current, end = " ")
        if(constraint == 'top'):
            if (graph.nodes[current]['AGE'] >= 28):
                result.append(current)
        if(constraint == 'med'):
            if (graph.nodes[current]['gender'] == 1):
                result.append(current)

        # Get all adjacent vertices of the
        # dequeued vertex s. If a adjacent
        # has not been visited, then mark it
        # visited and enqueue it
        for i in neighbor_info[current]:
            if visited[i - 1] == False:
                queue.append(i)
                visited[i - 1] = True 
    return result
top_arr = BFS(mgraph, mgraph.nodes[32]['user_id'], constraint='top')
print(top_arr)
med_graph = mgraph.subgraph(top_arr)
# print(med_graph.nodes[36])
med_arr = BFS(med_graph, med_graph.nodes[36]['user_id'], constraint='med')
print(med_arr)



