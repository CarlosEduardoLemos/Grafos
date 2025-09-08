import networkx as nx
import matplotlib.pyplot as plt
import os
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import argparse
import sys
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def create_output_dirs(base_dir: str) -> str:
    """Prepare IMG/img directory and return path to use."""
    img_dir_upper = os.path.join(base_dir, "IMG")
    img_dir_lower = os.path.join(base_dir, "img")
    if os.path.isdir(img_dir_upper):
        img_dir = img_dir_upper
    elif os.path.isdir(img_dir_lower):
        img_dir = img_dir_lower
    else:
        img_dir = img_dir_upper
        os.makedirs(img_dir_upper, exist_ok=True)
        os.makedirs(img_dir_lower, exist_ok=True)
    return img_dir

def save_fig(name: str, img_dir: str, dpi: int = 300) -> str:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{name}_{ts}.png"
    path = os.path.join(img_dir, filename)
    plt.savefig(path, bbox_inches='tight', dpi=dpi)
    logging.info(f"Figure saved: {path}")
    return path

def build_graph() -> nx.Graph:
    delivery_points = [
        "Asa Norte", "Asa Sul", "Lago Sul", "Esplanada", "Lago Norte", "Vila Planalto"
    ]
    connections = [
        ("Lago Sul", "Esplanada", 11),
        ("Lago Sul", "Asa Sul", 5),
        ("Lago Sul", "Vila Planalto", 14),
        ("Lago Norte", "Vila Planalto", 7),
        ("Lago Norte", "Esplanada", 8),
        ("Lago Norte", "Asa Norte", 12),
        ("Vila Planalto", "Esplanada", 10),
        ("Asa Norte", "Esplanada", 6),
        ("Asa Norte", "Asa Sul", 12),
        ("Asa Sul", "Esplanada", 5),
    ]
    G = nx.Graph()
    G.add_nodes_from(delivery_points)
    G.add_weighted_edges_from(connections)
    return G

def default_positions() -> Dict[str, Tuple[float, float]]:
    return {
        "Asa Norte": (-1.0,  0.0),
        "Asa Sul": (-0.6,  0.9),
        "Lago Sul": ( 0.6,  0.9),
        "Vila Planalto": ( 1.0,  0.0),
        "Lago Norte": ( 0.0, -0.9),
        "Esplanada":  ( 0.0,  0.15),
    }

def draw_graph(G: nx.Graph, pos: Dict[str, Tuple[float, float]], title: str, filename: str, img_dir: str):
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
    save_fig(filename, img_dir)
    plt.show()
    plt.close()

def highlight_shortest_path(G: nx.Graph, pos: Dict[str, Tuple[float, float]], path: List[str], title: str, filename: str, img_dir: str):
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
    save_fig(filename, img_dir)
    plt.show()
    plt.close()

def validate_nodes(G: nx.Graph, nodes: List[str]) -> bool:
    missing = [node for node in nodes if node not in G.nodes]
    if missing:
        logging.error(f"Node(s) not found in graph: {missing}")
        return False
    return True

def shortest_path_dijkstra(G: nx.Graph, source: str, target: str) -> Tuple[List[str], float]:
    path = nx.dijkstra_path(G, source=source, target=target, weight="weight")
    cost = nx.dijkstra_path_length(G, source=source, target=target, weight="weight")
    return path, cost

def all_shortest_paths_from(G: nx.Graph, source: str) -> None:
    logging.info(f"\nShortest paths from {source}:")
    for target in G.nodes:
        path = nx.dijkstra_path(G, source=source, target=target, weight="weight")
        cost = nx.dijkstra_path_length(G, source=source, target=target, weight="weight")
        logging.info(f"{source} -> {target}: path {path}, cost {cost}")

def tsp_approx(G: nx.Graph, nodes: Optional[List[str]] = None, cycle: bool = True) -> Tuple[List[str], float]:
    if nodes is None:
        nodes = list(G.nodes)
    tsp_cycle = nx.approximation.traveling_salesman_problem(G, nodes=nodes, weight="weight", cycle=cycle)
    cost = sum(G[tsp_cycle[i]][tsp_cycle[i+1]]['weight'] for i in range(len(tsp_cycle)-1))
    return tsp_cycle, cost

def parse_args(argv: List[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Delivery points graph analysis")
    p.add_argument("--no-draw", action="store_true", help="Do not draw or save figures")
    p.add_argument("--shortest", nargs=2, metavar=("SOURCE","TARGET"), help="Calculate and highlight shortest path")
    p.add_argument("--all-shortest-from", metavar="SOURCE", help="Print all shortest paths from SOURCE")
    p.add_argument("--tsp", action="store_true", help="Run TSP approximation")
    p.add_argument("--start", metavar="NODE", help="Optional start node for TSP/reports")
    return p.parse_args(argv)

def run_all(img_dir: str, args: argparse.Namespace):
    G = build_graph()
    pos = default_positions()

    if not args.no_draw:
        draw_graph(G, pos, "Graph - Carlos's Delivery Points", "full_graph", img_dir)

    # Shortest path example (default)
    if args.shortest:
        source, target = args.shortest
        if not validate_nodes(G, [source, target]):
            return
        path, cost = shortest_path_dijkstra(G, source, target)
        logging.info(f"Shortest path {source} -> {target}: {path} with cost {cost}")
        if not args.no_draw:
            highlight_shortest_path(G, pos, path, f"Graph - Shortest path: {source} → {target} (highlighted in red)", "shortest_path_graph", img_dir)
    else:
        # Default example
        source, target = "Lago Norte", "Lago Sul"
        path, cost = shortest_path_dijkstra(G, source, target)
        logging.info(f"Shortest path {source} -> {target}: {path} with cost {cost}")
        if not args.no_draw:
            highlight_shortest_path(G, pos, path, f"Graph - Shortest path: {source} → {target} (highlighted in red)", "shortest_path_graph", img_dir)

    # All shortest paths
    if args.all_shortest_from:
        if not validate_nodes(G, [args.all_shortest_from]):
            return
        all_shortest_paths_from(G, args.all_shortest_from)
    else:
        all_shortest_paths_from(G, "Lago Norte")

    # Always calculate TSP approximation and print value in reais
    try:
        tsp_cycle, tsp_cost = tsp_approx(G, nodes=list(G.nodes), cycle=True)
        logging.info(f"\nMost economical route (TSP): {tsp_cycle} with cost {tsp_cost}")
        total_value = tsp_cost * 20
        logging.info(f"Value in reais (multiplier 20) = R${total_value:.2f}")
    except Exception as e:
        logging.error(f"Failed to calculate TSP: {e}")

def main(argv: List[str] = None):
    base_dir = os.path.dirname(__file__) if '__file__' in globals() else os.getcwd()
    img_dir = create_output_dirs(base_dir)
    args = parse_args([] if argv is None else argv)
    try:
        run_all(img_dir, args)
    except nx.NetworkXNoPath as e:
        logging.error(f"Error: path not found - {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    main(sys.argv[1:])
