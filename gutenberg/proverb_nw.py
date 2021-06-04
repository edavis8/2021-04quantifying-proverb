import networkx as nx
import pandas as pd
import json
import copy
import numpy as np
from statsmodels.distributions.empirical_distribution import ECDF
import matplotlib.pyplot as plt

#file = open('./proverbs/gitdump/proverb_alldata2.txt')
#js = json.load(file)
#edge_list = dict()
#count = 0
#for book in js['all']:
#    common = []
#    non_proverbs = ['author', 'title', 'language', 'file']
#    title = book['title'][0] if book['title']!=[] else book['file']
#    ps = set(book.keys())
#    for x in non_proverbs:
#        ps.remove(x)
#    if ps != set():
#        for book2 in js['all']:
#            ps2 = set(book2.keys())
#            for x in non_proverbs:
#                ps2.remove(x)
#            if book2!=book:
#                if ps.intersection(ps2) != set():
#                    if book2['title'] != []:
#                        common += [book2['title'][0]]
#                    else:
#                        common += [book2['file']]
#    edge_list[title] = common
#    count +=1
#    print(count)
            
#with open('./proverbs/proverb_edge_list.json', 'w') as myfile:
#    json.dump(edge_list, myfile)

with open('./proverbs/proverb_edge_list.json', 'r') as myfile:
    book_edge = json.load(myfile)

G = nx.from_dict_of_lists(book_edge)
nx.write_gpickle(G, '.proverbs/book_edge_graph.pkl')
with open('./proverbs/book_nw_info.txt', 'w') as myfile:
    myfile.write(nx.info(G))
eig = nx.eigenvector_centrality(G)
l = list(eig.items())
l.sort(key = lambda x: x[1], reverse = True)
with open('.proverbs/book_nw_info.txt', 'a') as myfile:
    myfile.write(l[:100])
