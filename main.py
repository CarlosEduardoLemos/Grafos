import os
import argparse
import sys
import logging
from typing import List, Tuple, Optional
import networkx as nx
from graph_utils import build_graph, default_positions, validate_nodes
from visualization import draw_graph, highlight_shortest_path

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
MULTIPLIER_REAIS = 20  # Valor multiplicador para cálculo em reais

from graph_utils import build_graph, default_positions, validate_nodes
from visualization import draw_graph, highlight_shortest_path

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
    if args.shortest:
        if not validate_nodes(G, args.shortest):
            logging.error("Argumento inválido: um ou mais nós do menor caminho não existem no grafo.")
            logging.info(f"Nós válidos: {list(G.nodes)}")
            return 1
    if args.all_shortest_from:
        if not validate_nodes(G, [args.all_shortest_from]):
            logging.error("Argumento inválido: nó de origem para caminhos mínimos não existe no grafo.")
            logging.info(f"Nós válidos: {list(G.nodes)}")
            return 1
    if args.start:
        if not validate_nodes(G, [args.start]):
            logging.error("Argumento inválido: nó inicial para TSP/relatórios não existe no grafo.")
            logging.info(f"Nós válidos: {list(G.nodes)}")
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
    img_dir = os.path.join(base_dir, "IMG")
    os.makedirs(img_dir, exist_ok=True)
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

