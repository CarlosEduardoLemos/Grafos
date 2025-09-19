import matplotlib.pyplot as plt
import networkx as nx
from typing import Dict, Tuple, List

def draw_graph(G: nx.Graph, pos: Dict[str, Tuple[float, float]], title: str, filename: str, img_dir: str, show: bool = True):
    plt.figure(figsize=(8, 6))
    nx.draw_networkx_nodes(G, pos, node_size=2500, node_color="white", edgecolors="black", linewidths=2)
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight="bold")
    nx.draw_networkx_edges(G, pos, edge_color="tab:blue", width=2)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_color="tab:blue", font_size=10)
    plt.title(title, fontsize=14)
    plt.figtext(0.5, 0.01, "Figure 1 - Graph representing Carlos's delivery points", ha="center", fontsize=9, style="italic")
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(f"{img_dir}/{filename}.png", bbox_inches='tight', dpi=300)
    if show:
        plt.show()
    plt.close()

def highlight_shortest_path(G: nx.Graph, pos: Dict[str, Tuple[float, float]], path: List[str], title: str, filename: str, img_dir: str, show: bool = True):
    labels = nx.get_edge_attributes(G, 'weight')
    path_edges = list(zip(path, path[1:]))
    plt.figure(figsize=(8, 6))
    nx.draw_networkx_nodes(G, pos, node_size=2500, node_color="white", edgecolors="black", linewidths=2)
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight="bold")
    nx.draw_networkx_edges(G, pos, edge_color="lightgray", width=2)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_color="tab:blue", font_size=10)
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, width=4, edge_color="red")
    nx.draw_networkx_nodes(G, pos, nodelist=path, node_color="red", edgecolors="black", node_size=2500, linewidths=2)
    plt.title(title, fontsize=14)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(f"{img_dir}/{filename}.png", bbox_inches='tight', dpi=300)
    if show:
        plt.show()
    plt.close()
