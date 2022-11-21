# TopDownDPonGraphs
Top-Down Differential Privacy on Graphs

## About
Perform differential privacy on subcluster data of graph.<br/>
(todo)

## Visualization for Toy Example

Please run `visualization.ipynb` on jupyter notebook, the code is only compatible for jupyter notebook. <br>
This code will generate an interactive graph, with visible node attributes. <br>
Connected nodes means these two nodes are friend.

- [x] Translation on Pokec Dataset
- [ ] Data Cleaning
  
  * Have to device which attribute should be treated as sensitive information
  * have to add some synthetic data for missing values


## Notes on using the graph class


1. To create a graph with toy_example_500.csv, please run the function of utils.create_network()

```python
from utils import *

MAX_NODE=50
df = pd.read_csv('./toy_example_500.csv')
missing = load_missing()
graph = create_network(df, node_attributes, MAX_NODE, missing)
```
2. Get access to node information
```python

node_idx = 13 # the 13th node in the graph
attr='region' # the attribute u want to get access to
node_attribute = graph.nodes[node_index][attr]
```

3. Get access to neighbor members, this example will show you how to get access to the neighbor node with a given node
```python
from utils import *

neighbor_info = get_neighbor_information() # this is a dict like {node_idx: [neighbor_1, neighbor_2 ,...]}
# Let's say you want the indices of neighbors with node No.5:

neighbors = neighbor_info[5]
# this will return a list with all neighbor indices
```

4. After Searching all the nodes that meets the requirement e.g. (matches some attribute like gender == 1)
Then u will probabily get a list of node indices

U can run the following code to obtain a new subgraph w.r.t. these nodes

```python

node_matches = some_search_function(graph)

# node_matches = [1, 2, 4, 6]

subgraph = graph.subgraph(node_matches)
```

To run the search function, run <br>
`python DP.py -t region_large="Zilina Region" -m region_small="Kysucke New Town" -b hobbies="music"`
