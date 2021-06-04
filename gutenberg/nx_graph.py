import networkx as nx
import matplotlib.pyplot as plt
G = nx.read_gpickle("./proverbs/gitdump/component_1.pkl")
nx.draw(G, node_size = .5, width =0.01, node_color = 'b')
plt.title("Large Connected Subcomponent \n (proverbs as nodes)")
plt.savefig("./proverbs/large_subgraph.png", dpi = 600)
