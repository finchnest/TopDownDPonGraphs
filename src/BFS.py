from platform import node
from turtle import clear
import pandas as pd
import sys
import os
import random
from RelationalOp import RelationalOp
import copy

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)


import utils 

vis_attributes = ['user_id', 'public', 'completion_percentage', 'gender', 'last_login', 'age', 'body', 'I_am_working_in_field', 'spoken_languages', 'hobbies', 'region_large', 'region_small', 'height', 'weight']

missing = utils.load_missing()
df = pd.read_csv(parent+'/data/target_data.csv')
# print(df.head())
# print(len(df['height']))

mgraph = utils.create_network(df, vis_attributes, 20000, missing)
edge_df = pd.read_csv(parent+'/data/example_edge_20k.csv')
neighbor_info = utils.get_neighbor_information(edge_df) 

# print(mgraph.nodes[1])

# print(len(list(mgraph.nodes))) 
# print(len(df)) 

#the line below necessary b/c of inconsistencies in the .csv file.
size = 20073

def preBFS(appArgs):
    global top_key, top_value, med_key, med_value, bot_key, bot_value, bot_ops

    top_key = appArgs.top[0].key
    top_value = appArgs.top[0].value
    # top_ops = appArgs.top[0].relationalOp

    med_key = appArgs.med[0].key
    med_value = appArgs.med[0].value
    # med_ops = appArgs.med[0].relationalOp

    bot_key = appArgs.bot[0].key
    bot_value = appArgs.bot[0].value
    bot_ops = appArgs.bot[0].relationalOp

    return BFS(mgraph, mgraph.nodes[1]['user_id'])



def BFS(graph, source_node):

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
           
        if (bot_key and graph.nodes[current]):
            # print(graph.nodes[current])
            if (graph.nodes[current][top_key] == top_value and graph.nodes[current][med_key] == med_value):
                if(bot_ops == RelationalOp.EQUAL):
                    if (graph.nodes[current][bot_key] == int(bot_value)):
                        result.append(current)

                elif (bot_ops == RelationalOp.GREAT_THAN):
                    if (graph.nodes[current][bot_key] > int(bot_value)):
                        result.append(current)

                elif (bot_ops == RelationalOp.LESS_THAN):
                    if (graph.nodes[current][bot_key] < int(bot_value)):
                        result.append(current)

                elif (bot_ops == RelationalOp.LESS_THAN_EQ):
                    if (graph.nodes[current][bot_key] <= int(bot_value)):
                        result.append(current)

                else:
                    if (graph.nodes[current][bot_key] >= int(bot_value)):
                        result.append(current)
        else:

            if (graph.nodes[current] and med_key and graph.nodes[current][top_key] == top_value and graph.nodes[current][med_key] == med_value):
                result.append(current)
            elif(graph.nodes[current] and graph.nodes[current][top_key] == top_value):
                result.append(current)


        # Get all adjacent vertices of the
        # dequeued vertex.
        for i in neighbor_info[current]:
            # print(i)
            #the line below necessary b/c of inconsistencies in the .csv file.
            if(i >= 20073):
                continue
            if visited[i - 1] == False:
                queue.append(i)
                visited[i - 1] = True 
    return (result, len(result))

