import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('./apriori.csv')

#  element = map(lambda x: x[0], df[['A']].values)
DG = nx.Graph()
#  DG.add_nodes_from(element)
DG.add_edges_from(df[['A','B']].values)

pos=nx.circular_layout(DG)

nx.draw_networkx_nodes(DG, pos, alpha=0.2, node_size=1000, node_color='0.75')
nx.draw_networkx_edges(DG, pos, alpha=0.1)
nx.draw_networkx_labels(DG, pos, font_family='sans-serif', font_size=8)

plt.axis("off")
plt.margins(0.1)
plt.show()
