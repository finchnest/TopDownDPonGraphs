import pandas as pd
from tqdm import tqdm
import numpy as np
import re
import html
from urllib import parse
import requests
import networkx
from bokeh.io import output_notebook, show, save

from bokeh.io import output_notebook, show, save
from bokeh.models import Range1d, Circle, ColumnDataSource, MultiLine
from bokeh.plotting import figure
from bokeh.plotting import from_networkx

def parse_relation(relationships):
    res = []
    for line in relationships:
        line = line.split('\t')
        res.append([line[0], line[1]])
    return res

def parse_row(row):
    row = row.split('\t')
    row = row[:-1]
    return row

def load_missing():
    with open('/Users/abeni/Projects/397-DP-Code/TopDownDPonGraphs/missing_users.txt', 'rb') as f:
        lines = f.readlines()
    lst = [int(l.replace(b'\n', b'')) for l in lines]
    return lst

def get_node_attribute(graph, node_index, attribute_key):
    
    # graph: the networkx graph
    # node_index: (int), the index for the node u want to get access to
    # attribute_key: (str), the attribute you want to get access to e.g. 'gender', 'region'
    
    return graph.nodes[node_index][attribute_key]

def get_neighbor_information(edge_path='/Users/abeni/Projects/397-DP-Code/TopDownDPonGraphs/toy_example_edge_50.csv'):
    
    missing_user = load_missing()
    edge_df = pd.read_csv(edge_path)
    src = edge_df['source'].tolist()
    tgt = edge_df['target'].tolist()
    
    neighbors = {}
    for i in range(len(src)):
        if src[i] not in missing_user and tgt[i] not in missing_user:
            if src[i] in neighbors:
                neighbors[src[i]].append(tgt[i])
            else:
                neighbors[src[i]] = [tgt[i]]
            
            if tgt[i] in neighbors:
                neighbors[tgt[i]].append(src[i])
            else:
                neighbors[tgt[i]] = [src[i]]
    
    for k in neighbors.keys():
        neighbors[k] = list(set(neighbors[k]))

    return neighbors

def create_network(profiles, attr, max_node, empty_user):
    
    net = get_graph_edge(max_node, empty_user)
    # profiles : dataframe

    all_attrs = {}
    for idx, p in profiles.iterrows():
        node_attr = row_to_dict(p, attr)
        node_id = int(p['user_id'])
        if node_id <= max_node:
            all_attrs[node_id] = node_attr
    networkx.set_node_attributes(net, all_attrs)
    return net

def load_from_csv(path):
    df = pd.read_csv(path)
    return df

def row_to_dict(row, attr):
    data = {}
    for a in attr:
        data[a] = row[a]
    return data

def get_graph_edge(max_node=20, empty_user=[]):
    
    edge_df = pd.read_csv('/Users/abeni/Projects/397-DP-Code/TopDownDPonGraphs/toy_example_edge_50.csv')
    G = networkx.from_pandas_edgelist(edge_df, 'source', 'target')
    # print('Edge Amount of this graph:', len(edge_df))
    return G
    
def get_subgraph(graph, nodes):

    # graph: oroginal graph
    # nodes: a list of node indices in subgraph

    subgraph = copy.copy(graph)
    origin_nodes = graph.nodes
    to_remove = [n for n in origin_nodes if n not in nodes]
    subgraph.remove_nodes_from(to_remove)
    return subgraph
