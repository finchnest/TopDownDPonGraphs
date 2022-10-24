import pandas as pd
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

neighbor_info = utils.get_neighbor_information() 

constraint = {"top": 'age>28', "gender": 1}

'''
top constraint: age>=28
medium constraint: gender = 1
'''

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

        current = queue.pop(0)
        if(constraint == 'top'):
            if (graph.nodes[current]['AGE'] >= 28):
                result.append(current)
        if(constraint == 'med'):
            if (graph.nodes[current]['gender'] == 1):
                result.append(current)

        # Get all adjacent vertices of the
        # dequeued vertex.
        for i in neighbor_info[current]:
            if visited[i - 1] == False:
                queue.append(i)
                visited[i - 1] = True 
    return result
top_arr = BFS(mgraph, mgraph.nodes[32]['user_id'], constraint='top')
print(top_arr[0])
med_graph = mgraph.subgraph(top_arr)
# print(med_graph.nodes[36])
med_arr = BFS(med_graph, med_graph.nodes[top_arr[0]]['user_id'], constraint='med')
print(med_arr)



