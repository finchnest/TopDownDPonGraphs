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


def get_graph_edge(relationships, max_node=20):
    
    pairs = parse_relation(relationships)

    src, tgt = [], []
    for p in pairs:
        if int(p[0]) <= max_node and int(p[1]) <= max_node:
            s, t = int(p[0]), int(p[1])
            src.append(s)
            tgt.append(t)
    data = {'source':src, 'target': tgt}
    edge_df = pd.DataFrame(data)
    edge_df.to_csv('./toy_example_edge.csv', index=False)
    G = networkx.from_pandas_edgelist(edge_df, 'source', 'target')
    print('Edge Amount of this graph:', len(src))
    return G

def translate(text, to_language="en", text_language="sk"):

    GOOGLE_TRANSLATE_URL = 'http://translate.google.sk/m?q=%s&tl=%s&sl=%s'

    text = parse.quote(text)
    url = GOOGLE_TRANSLATE_URL % (text,to_language,text_language)
    response = requests.get(url)
    data = response.text
    expr = r'(?s)class="(?:t0|result-container)">(.*?)<'
    result = re.findall(expr, data)
    if (len(result) == 0):
        return ""

    return html.unescape(result[0])

def parse_row(row):
    row = row.split('\t')
    row = row[:-1]
    return row


def create_network(profiles, relationships, attr, max_node):
    
    net = get_graph_edge(relationships, max_node)
    # profiles = [parse_row(p) for p in profiles]

    # profiles : dataframe

    all_attrs = {}
    for idx, p in profiles:
        node_attr = row_to_dict(p)
        for i, v in enumerate(p):
            # index, value
            if v.isnumeric():
                v = int(v)
            if v != 'null':
                node_attr[attr[i]] = v
        node_id = int(p[0])
        all_attrs[node_id] = node_attr
    networkx.set_node_attributes(net, all_attrs)
    return net

# def create_network(profiles, relationships, attr, max_node):
    
#     net = get_graph_edge(relationships, max_node)
#     for i, a in enumerate(attr):
#         if i != 0:     
#             print(a)
#             values = [p[i] for p in profiles]
#             print(values)
#             networkx.set_node_attributes(net, name=a, values=values)

#     return net