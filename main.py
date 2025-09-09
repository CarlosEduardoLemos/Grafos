import networkx as nx
import matplotlib.pyplot as plt
import os
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import argparse
import sys
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

MULTIPLIER_REAIS = 20  # Valor multiplicador para cálculo em reais

def create_output_dirs(base_dir: str) -> str:
    """Cria diretório IMG para salvar imagens."""
    img_dir = os.path.join(base_dir, "IMG")
    os.makedirs(img_dir, exist_ok=True)
    return img_dir

def save_fig(name: str, img_dir: str, dpi: int = 300) -> str:
    """Salva a figura atual do matplotlib no diretório especificado."""
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{name}_{ts}.png"
    path = os.path.join(img_dir, filename)
    plt.savefig(path, bbox_inches='tight', dpi=dpi)
    logging.info(f"Figure saved: {path}")
    return path

def build_graph() -> nx.Graph:
    """Constrói o grafo dos pontos de entrega e suas conexões."""
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
    """Retorna posições fixas para os nós do grafo."""
    return {
        "Asa Norte": (-1.0,  0.0),
        "Asa Sul": (-0.6,  0.9),
        "Lago Sul": ( 0.6,  0.9),
        "Vila Planalto": ( 1.0,  0.0),
        "Lago Norte": ( 0.0, -0.9),
        "Esplanada":  ( 0.0,  0.15),
    }

def draw_graph(G: nx.Graph, pos: Dict[str, Tuple[float, float]], title: str, filename: str, img_dir: str, show: bool = True):
    """Desenha o grafo e salva a imagem. Mostra na tela se show=True."""
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
    if show:
        plt.show()
    plt.close()

def highlight_shortest_path(G: nx.Graph, pos: Dict[str, Tuple[float, float]], path: List[str], title: str, filename: str, img_dir: str, show: bool = True):
    """Desenha o grafo destacando o caminho mais curto."""
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
    if show:
        plt.show()
    plt.close()

def validate_nodes(G: nx.Graph, nodes: List[str]) -> bool:
    """Valida se os nós existem no grafo."""
    missing = [node for node in nodes if node not in G.nodes]
    if missing:
        logging.error(f"Node(s) not found in graph: {missing}")
        return False
    return True

def shortest_path_dijkstra(G: nx.Graph, source: str, target: str) -> Tuple[List[str], float]:
    """Calcula o caminho mais curto entre dois nós usando Dijkstra."""
    path = nx.dijkstra_path(G, source=source, target=target, weight="weight")
    cost = nx.dijkstra_path_length(G, source=source, target=target, weight="weight")
    return path, cost

def all_shortest_paths_from(G: nx.Graph, source: str) -> None:
    """Exibe todos os caminhos mais curtos a partir de um nó."""
    logging.info(f"\nShortest paths from {source}:")
    for target in G.nodes:
        path = nx.dijkstra_path(G, source=source, target=target, weight="weight")
        cost = nx.dijkstra_path_length(G, source=source, target=target, weight="weight")
        logging.info(f"{source} -> {target}: path {path}, cost {cost}")

def tsp_approx(G: nx.Graph, nodes: Optional[List[str]] = None, cycle: bool = True) -> Tuple[List[str], float]:
    """Calcula uma solução aproximada para o TSP."""
    if nodes is None:
        nodes = list(G.nodes)
    tsp_cycle = nx.approximation.traveling_salesman_problem(G, nodes=nodes, weight="weight", cycle=cycle)
    cost = sum(G[tsp_cycle[i]][tsp_cycle[i+1]]['weight'] for i in range(len(tsp_cycle)-1))
    return tsp_cycle, cost

def parse_args(argv: List[str]) -> argparse.Namespace:
    """Processa os argumentos da linha de comando."""
    p = argparse.ArgumentParser(description="Delivery points graph analysis")
    p.add_argument("--no-draw", action="store_true", help="Do not draw or save figures")
    p.add_argument("--shortest", nargs=2, metavar=("SOURCE","TARGET"), help="Calculate and highlight shortest path")
    p.add_argument("--all-shortest-from", metavar="SOURCE", help="Print all shortest paths from SOURCE")
    p.add_argument("--tsp", action="store_true", help="Run TSP approximation")
    p.add_argument("--start", metavar="NODE", help="Optional start node for TSP/reports")
    p.add_argument("--show", action="store_true", help="Show figures interactively")
    return p.parse_args(argv)

def run_all(img_dir: str, args: argparse.Namespace) -> int:
    """Executa todas as análises e visualizações. Retorna código de erro."""
    G = build_graph()
    pos = default_positions()
    show_figs = args.show and not args.no_draw

    # Validação dos argumentos
    if args.shortest and not validate_nodes(G, args.shortest):
        return 1
    if args.all_shortest_from and not validate_nodes(G, [args.all_shortest_from]):
        return 1
    if args.start and not validate_nodes(G, [args.start]):
        return 1

    if not args.no_draw:
        draw_graph(G, pos, "Graph - Carlos's Delivery Points", "full_graph", img_dir, show=show_figs)

    # Shortest path
    if args.shortest:
        source, target = args.shortest
        path, cost = shortest_path_dijkstra(G, source, target)
        logging.info(f"Shortest path {source} -> {target}: {path} with cost {cost}")
        if not args.no_draw:
            highlight_shortest_path(G, pos, path, f"Graph - Shortest path: {source} → {target} (highlighted in red)", "shortest_path_graph", img_dir, show=show_figs)
    else:
        source, target = "Lago Norte", "Lago Sul"
        path, cost = shortest_path_dijkstra(G, source, target)
        logging.info(f"Shortest path {source} -> {target}: {path} with cost {cost}")
        if not args.no_draw:
            highlight_shortest_path(G, pos, path, f"Graph - Shortest path: {source} → {target} (highlighted in red)", "shortest_path_graph", img_dir, show=show_figs)

    # All shortest paths
    if args.all_shortest_from:
        all_shortest_paths_from(G, args.all_shortest_from)
    else:
        all_shortest_paths_from(G, "Lago Norte")

    # TSP
    try:
        tsp_cycle, tsp_cost = tsp_approx(G, nodes=list(G.nodes), cycle=True)
        logging.info(f"\nMost economical route (TSP): {tsp_cycle} with cost {tsp_cost}")
        total_value = tsp_cost * MULTIPLIER_REAIS
        logging.info(f"Value in reais (multiplier {MULTIPLIER_REAIS}) = R${total_value:.2f}")
    except Exception as e:
        logging.error(f"Failed to calculate TSP: {e}")
        return 2

    return 0

def main(argv: List[str] = None) -> int:
    """Função principal. Retorna código de erro."""
    base_dir = os.path.dirname(__file__) if '__file__' in globals() else os.getcwd()
    img_dir = create_output_dirs(base_dir)
    args = parse_args([] if argv is None else argv)
    try:
        return run_all(img_dir, args)
    except nx.NetworkXNoPath as e:
        logging.error(f"Error: path not found - {e}")
        return 3
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return 4

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

