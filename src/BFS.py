import pandas as pd
import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import utils


edge_df = pd.read_csv(parent+'/data/example_edge_20k.csv')
neighbor_info = utils.get_neighbor_information(edge_df)

#the line below necessary b/c of inconsistencies in the .csv file.
size = 20073

def BFS(graph, appArgs):
    source_node = graph.nodes[1]['user_id']
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
        node = graph.nodes[current]
        if not node:
            continue

        # check all top constraints using relational operator
        topPass = all(top.relationalOp.value[1](node[top.key], top.value) for top in appArgs.top)

        # check all med constraints using relational operator
        medPass = all(med.relationalOp.value[1](node[med.key], med.value) for med in appArgs.med)

        # check all bot constraints using relational operator
        botPass = all(bot.relationalOp.value[1](node[bot.key], int(bot.value)) for bot in appArgs.bot)

        # add current if all checks passed
        if topPass and medPass and botPass:
            result.append(current)

        # Get all adjacent vertices of the
        # dequeued vertex.
        for i in neighbor_info[current]:
            # print(i)
            #the line below necessary b/c of inconsistencies in the .csv file.
            if(i >= size):
                continue
            if visited[i - 1] == False:
                queue.append(i)
                visited[i - 1] = True

    return result
