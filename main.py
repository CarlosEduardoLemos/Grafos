import networkx as nx
import matplotlib.pyplot as plt
import os
from datetime import datetime
from typing import Dict, List, Tuple

# Diretório base do arquivo
base_dir = os.path.dirname(__file__) if '__file__' in globals() else os.getcwd()

# Criar pastas para salvar imagens: prioriza "IMG" (maiúscula), mas também garante "img" por compatibilidade
img_dir_upper = os.path.join(base_dir, "IMG")
img_dir_lower = os.path.join(base_dir, "img")

# Se uma das pastas já existir, use-a; caso contrário crie "IMG" e também crie "img" para compatibilidade
if os.path.isdir(img_dir_upper):
    img_dir = img_dir_upper
elif os.path.isdir(img_dir_lower):
    img_dir = img_dir_lower
else:
    img_dir = img_dir_upper
    os.makedirs(img_dir_upper, exist_ok=True)
    os.makedirs(img_dir_lower, exist_ok=True)

def save_fig(name: str, dpi: int = 300) -> str:
    """Salva a figura matplotlib atual em img/<name>_YYYYMMDD_HHMMSS.png"""
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{name}_{ts}.png"
    path = os.path.join(img_dir, filename)
    plt.savefig(path, bbox_inches='tight', dpi=dpi)
    print(f"Figura salva: {path}")
    return path

def build_graph() -> nx.Graph:
    """Cria e retorna o grafo com nós e arestas ponderadas."""
    locais_entrega = [
        "Asa Norte", "Asa Sul", "Lago Sul", "Esplanada", "Lago Norte", "Vila Planalto"
    ]
    conexoes = [
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
    G.add_nodes_from(locais_entrega)
    G.add_weighted_edges_from(conexoes)
    return G

def default_positions() -> Dict[str, Tuple[float, float]]:
    """Posições manuais para reproduzir a figura fornecida."""
    return {
        "Asa Norte": (-1.0,  0.0),
        "Asa Sul":   (-0.6,  0.9),
        "Lago Sul":  ( 0.6,  0.9),
        "Vila Planalto": ( 1.0,  0.0),
        "Lago Norte": ( 0.0, -0.9),
        "Esplanada":  ( 0.0,  0.15),
    }

def draw_graph(G: nx.Graph, pos: Dict[str, Tuple[float, float]], title: str, filename: str):
    """Desenha o grafo completo e salva a figura."""
    plt.figure(figsize=(8, 6))
    nx.draw_networkx_nodes(
        G, pos,
        node_size=2500,
        node_color="white",
        edgecolors="black",
        linewidths=2
    )
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight="bold")
    nx.draw_networkx_edges(G, pos, edge_color="tab:blue", width=2)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_color="tab:blue", font_size=10)
    plt.title(title, fontsize=14)
    plt.figtext(0.5, 0.01, "Figura 1 - Grafo representando os pontos de entrega de Carlos", ha="center", fontsize=9, style="italic")
    plt.axis('off')
    plt.tight_layout()
    save_fig(filename)
    plt.show()
    plt.close()

def highlight_shortest_path(G: nx.Graph, pos: Dict[str, Tuple[float, float]], path: List[str], title: str, filename: str):
    """Desenha o grafo e destaca um caminho (lista de nós) em vermelho."""
    labels = nx.get_edge_attributes(G, 'weight')
    path_edges = list(zip(path, path[1:]))
    plt.figure(figsize=(8, 6))
    nx.draw_networkx_nodes(
        G, pos,
        node_size=2500,
        node_color="white",
        edgecolors="black",
        linewidths=2
    )
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight="bold")
    nx.draw_networkx_edges(G, pos, edge_color="lightgray", width=2)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_color="tab:blue", font_size=10)
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, width=4, edge_color="red")
    nx.draw_networkx_nodes(G, pos, nodelist=path, node_color="red", edgecolors="black", node_size=2500, linewidths=2)
    plt.title(title, fontsize=14)
    plt.axis('off')
    plt.tight_layout()
    save_fig(filename)
    plt.show()
    plt.close()

def shortest_path_dijkstra(G: nx.Graph, source: str, target: str) -> Tuple[List[str], float]:
    """Retorna (caminho, custo) usando Dijkstra considerando o peso 'weight'."""
    caminho = nx.dijkstra_path(G, source=source, target=target, weight="weight")
    custo = nx.dijkstra_path_length(G, source=source, target=target, weight="weight")
    return caminho, custo

def all_shortest_paths_from(G: nx.Graph, source: str) -> None:
    """Imprime os caminhos mínimos a partir de `source` para todos os nós do grafo."""
    print(f"\nCaminhos mínimos a partir de {source}:")
    for destino in G.nodes:
        caminho = nx.dijkstra_path(G, source=source, target=destino, weight="weight")
        custo = nx.dijkstra_path_length(G, source=source, target=destino, weight="weight")
        print(f"{source} -> {destino}: caminho {caminho}, custo {custo}")

def tsp_approx(G: nx.Graph, nodes: List[str] = None, cycle: bool = True) -> Tuple[List[str], float]:
    """Retorna (rota, custo) aproximada do TSP. Se nodes for None usa todos os nós."""
    if nodes is None:
        nodes = list(G.nodes)
    ciclo = nx.approximation.traveling_salesman_problem(G, nodes=nodes, weight="weight", cycle=cycle)
    custo = sum(G[ciclo[i]][ciclo[i+1]]['weight'] for i in range(len(ciclo)-1))
    return ciclo, custo

def main():
    G = build_graph()
    pos = default_positions()

    # 1) Desenhar grafo completo
    draw_graph(G, pos, "Grafo - Pontos de Entrega de Carlos", "grafo_completo")

    # 2) Menor caminho entre dois pontos (exemplo Lago Norte -> Lago Sul)
    origem, destino = "Lago Norte", "Lago Sul"
    caminho, custo = shortest_path_dijkstra(G, origem, destino)
    print(f"Menor caminho {origem} -> {destino}: {caminho} com custo {custo}")
    highlight_shortest_path(G, pos, caminho, f"Grafo - Menor caminho: {origem} → {destino} (destacado em vermelho)", "grafo_menor_caminho")

    # 3) Todos os menores caminhos a partir de Lago Norte
    all_shortest_paths_from(G, "Lago Norte")

    # 4) TSP (aproximação) para todos os nós
    tsp_ciclo, tsp_custo = tsp_approx(G, nodes=list(G.nodes), cycle=True)
    print(f"\nCaminho mais econômico (TSP): {tsp_ciclo} com custo {tsp_custo}")

    # 5) Exemplo de custo monetário saindo da Esplanada
    tsp_espl, tsp_espl_custo = tsp_approx(G, nodes=list(G.nodes), cycle=True)
    valor_total = tsp_espl_custo * 20
    print(f"\nSaindo da Esplanada, custo total = {tsp_espl_custo}, valor em reais = R${valor_total:.2f}")

if __name__ == "__main__":
    main()
