import pandas as pd
from tqdm import tqdm
import networkx
import matplotlib.pyplot as plt
import random

import os
import copy

current = os.path.dirname(os.path.realpath(__file__))
print(current)

def search_missing():

    df = pd.read_csv('./data/top_20000.csv')
    missing = []
    ids = df['user_id'].tolist()
    for i in range(20000):
        if i not in ids:
            missing.append(i)
    with open('./data/missing_user.txt', 'wb') as f:
        for m in missing:
            f.write(str(m)+'\n')

#def simple_plot_with_idx(graph, save_path):
#
#    networkx.draw_networkx(g)
#    plt.savefig(save_path)

def cleaning(df):

    # step 0: splitting certain columns

    region = list(df['region'])
    region_big = [r.split(', ')[0] for r in region]
    region_small = [r.split(', ')[1] for r in region]
    df['region_large'] = region_big
    df['region_small'] = region_small

    # step 1: cleaning null values
    cols = df.columns

    replace_dict = {c:[] for c in cols}

    for i, row in df.iterrows():
        for c in cols:
            if row[c] == 'null':
                replace_dict[c].append(i)

    for c in cols:
        vals = df[c].unique()
        try:
            vals.remove('null')
        except:
            pass
        for idx in replace_dict[c]:
            df[c][idx] = random.choice(vals)

    # step 2: create height and weight
    body = list(df['body'])
    height = [b.split(', ')[0] for b in body]
    weight = [b.split(', ')[1] for b in body]
    df['height'] = region_big
    df['weight'] = region_small

    df.to_csv('clean_data_full.csv')
    special = ['user_id', 'public', 'completion_percentage', 'gender', 'region', 'last_login',
        'registration', 'AGE', 'body', 'I_am_working_in_field', 'spoken_languages', 'hobbies',
        'height', 'weight', 'region_large', 'region_small']
    target_data = {s:list(df[s]) for s in special}
    target_df = pd.DataFrame(target_data)
    target_df.to_csv('target_data.csv', index=False)

def save_graph_edge(missing):

    data_df = pd.read_csv('./data/target_data.csv')
    user_ids = data_df['user_id'].tolist()
    user_ids = [int(i) for i in user_ids]
    with open('./soc-pokec-relationships.txt') as f:
        lines = f.readlines()
    pairs = parse_relation(lines)
    src, tgt = [], []
    for p in tqdm(pairs):
        s,t = int(p[0]), int(p[1])
        if s <= 20073 and t <= 20073:
            if s not in missing and t not in missing:
                if s in user_ids and t in user_ids:
                    src.append(int(s))
                    tgt.append(int(t))

    data = {'source':src, 'target':tgt}
    df = pd.DataFrame(data)
    df.to_csv('./example_edge_20k.csv', index=False)

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
    with open(current+'/data/missing_user.txt', 'rb') as f:
        lines = f.readlines()
    lst = [int(l.replace(b'\n', b'')) for l in lines]
    return lst

def get_node_attribute(graph, node_index, attribute_key):

    # graph: the networkx graph
    # node_index: (int), the index for the node u want to get access to
    # attribute_key: (str), the attribute you want to get access to e.g. 'gender', 'region'

    return graph.nodes[node_index][attribute_key]

def get_neighbor_information(edge_df):

    missing_user = load_missing()
    # edge_df = pd.read_csv(edge_path)
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

    edge_df = pd.read_csv(current+'/data/example_edge_20k.csv')
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

def load_missing():
    with open(current+'/data/missing_user.txt') as f:
        lines = f.readlines()
    lst = [int(l.replace('\n', '')) for l in lines]
    return lst

# missing = load_missing()
# save_graph_edge(missing)