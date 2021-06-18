



import networkx as nx
import json

G = nx.read_gpickle('./proverbs/gitdump/author_graph.pkl')

between = nx.algorithms.betweenness_centrality(G)

closeness  = nx.algoritms.closeness_centrailty(G)

with open('./proverbs/gitdump/author_btwn.json') as file:
    json.dump(between, file)

with open('./proverbs/gitdump/author_close.json') as file:
    json.dump(closeness, file)
