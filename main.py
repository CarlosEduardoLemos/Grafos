import networkx as nx
import matplotlib.pyplot as plt
import os
from datetime import datetime
from typing import Dict, List, Tuple

# Arquivo principal para criar e analisar um grafo de pontos de entrega,
# desenhar o grafo, calcular menores caminhos e uma aproximação do TSP.

# Diretório base do arquivo (arquivo em execução) — usado para salvar imagens
base_dir = os.path.dirname(__file__) if '__file__' in globals() else os.getcwd()

# Preparação dos diretórios de saída para imagens.
# Prioriza "IMG" (maiúsculo) mas também garante "img" (minúsculo) por compatibilidade.
img_dir_upper = os.path.join(base_dir, "IMG")
img_dir_lower = os.path.join(base_dir, "img")

# Se uma das pastas já existir, use-a; caso contrário crie ambas.
if os.path.isdir(img_dir_upper):
    img_dir = img_dir_upper
elif os.path.isdir(img_dir_lower):
    img_dir = img_dir_lower
else:
    img_dir = img_dir_upper
    os.makedirs(img_dir_upper, exist_ok=True)
    os.makedirs(img_dir_lower, exist_ok=True)

def save_fig(name: str, dpi: int = 300) -> str:
    """Salva a figura matplotlib atual em img/<name>_YYYYMMDD_HHMMSS.png.
    Retorna o caminho do arquivo salvo."""
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{name}_{ts}.png"
    path = os.path.join(img_dir, filename)
    plt.savefig(path, bbox_inches='tight', dpi=dpi)
    print(f"Figura salva: {path}")
    return path

def build_graph() -> nx.Graph:
    """Cria e retorna o grafo não-direcionado com nós e arestas ponderadas.
    Nós representam locais de entrega e as arestas têm atributo 'weight' (distância/custo)."""
    locais_entrega = [
        "Asa Norte", "Asa Sul", "Lago Sul", "Esplanada", "Lago Norte", "Vila Planalto"
    ]
    # Cada tupla: (nó1, nó2, peso)
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
    G.add_nodes_from(locais_entrega)         # adiciona nós
    G.add_weighted_edges_from(conexoes)     # adiciona arestas com peso
    return G

def default_positions() -> Dict[str, Tuple[float, float]]:
    """Posições fixas (x, y) para desenhar o grafo de forma consistente."""
    return {
        "Asa Norte": (-1.0,  0.0),
        "Asa Sul":   (-0.6,  0.9),
        "Lago Sul":  ( 0.6,  0.9),
        "Vila Planalto": ( 1.0,  0.0),
        "Lago Norte": ( 0.0, -0.9),
        "Esplanada":  ( 0.0,  0.15),
    }

def draw_graph(G: nx.Graph, pos: Dict[str, Tuple[float, float]], title: str, filename: str):
    """Desenha o grafo completo (todos os nós e arestas) e salva a imagem.
    - G: grafo
    - pos: posições dos nós
    - title: título da figura
    - filename: prefixo do arquivo salvo"""
    plt.figure(figsize=(8, 6))
    # Desenha nós com borda preta e fundo branco
    nx.draw_networkx_nodes(
        G, pos,
        node_size=2500,
        node_color="white",
        edgecolors="black",
        linewidths=2
    )
    # Rótulos dos nós
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight="bold")
    # Arestas em azul
    nx.draw_networkx_edges(G, pos, edge_color="tab:blue", width=2)
    # Rótulos de peso nas arestas
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_color="tab:blue", font_size=10)
    plt.title(title, fontsize=14)
    # Texto descritivo na figura
    plt.figtext(0.5, 0.01, "Figura 1 - Grafo representando os pontos de entrega de Carlos", ha="center", fontsize=9, style="italic")
    plt.axis('off')
    plt.tight_layout()
    save_fig(filename)   # salva a figura atual
    plt.show()
    plt.close()

def highlight_shortest_path(G: nx.Graph, pos: Dict[str, Tuple[float, float]], path: List[str], title: str, filename: str):
    """Desenha o grafo e destaca um caminho específico (lista de nós) em vermelho.
    - path: lista ordenada de nós que formam o caminho a ser destacado"""
    labels = nx.get_edge_attributes(G, 'weight')
    path_edges = list(zip(path, path[1:]))  # pares de arestas que compõem o caminho
    plt.figure(figsize=(8, 6))
    # Desenha todos os nós e arestas em cores neutras
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
    # Destaca as arestas do caminho em vermelho e os nós do caminho preenchidos em vermelho
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, width=4, edge_color="red")
    nx.draw_networkx_nodes(G, pos, nodelist=path, node_color="red", edgecolors="black", node_size=2500, linewidths=2)
    plt.title(title, fontsize=14)
    plt.axis('off')
    plt.tight_layout()
    save_fig(filename)
    plt.show()
    plt.close()

def shortest_path_dijkstra(G: nx.Graph, source: str, target: str) -> Tuple[List[str], float]:
    """Calcula menor caminho e custo entre source e target usando Dijkstra (peso 'weight')."""
    caminho = nx.dijkstra_path(G, source=source, target=target, weight="weight")
    custo = nx.dijkstra_path_length(G, source=source, target=target, weight="weight")
    return caminho, custo

def all_shortest_paths_from(G: nx.Graph, source: str) -> None:
    """Imprime no console os caminhos mínimos e seus custos a partir de 'source' para todos os nós."""
    print(f"\nCaminhos mínimos a partir de {source}:")
    for destino in G.nodes:
        caminho = nx.dijkstra_path(G, source=source, target=destino, weight="weight")
        custo = nx.dijkstra_path_length(G, source=source, target=destino, weight="weight")
        print(f"{source} -> {destino}: caminho {caminho}, custo {custo}")

def tsp_approx(G: nx.Graph, nodes: List[str] = None, cycle: bool = True) -> Tuple[List[str], float]:
    """Retorna (rota, custo) aproximada do problema do caixeiro viajante (TSP).
    Usa a aproximação do NetworkX. Se 'nodes' for None usa todos os nós.
    'cycle' indica se o resultado deve fechar o ciclo (retornar ao ponto inicial)."""
    if nodes is None:
        nodes = list(G.nodes)
    # nx.approximation.traveling_salesman_problem retorna um ciclo/rota aproximada
    ciclo = nx.approximation.traveling_salesman_problem(G, nodes=nodes, weight="weight", cycle=cycle)
    # soma custos entre pares consecutivos na rota retornada
    custo = sum(G[ciclo[i]][ciclo[i+1]]['weight'] for i in range(len(ciclo)-1))
    return ciclo, custo

def main():
    # Cria o grafo e define posições fixas para desenho
    G = build_graph()
    pos = default_positions()

    # 1) Desenhar grafo completo e salvar imagem
    draw_graph(G, pos, "Grafo - Pontos de Entrega de Carlos", "grafo_completo")

    # 2) Menor caminho entre dois pontos (exemplo: Lago Norte -> Lago Sul)
    origem, destino = "Lago Norte", "Lago Sul"
    caminho, custo = shortest_path_dijkstra(G, origem, destino)
    print(f"Menor caminho {origem} -> {destino}: {caminho} com custo {custo}")
    # Desenha o grafo destacando o menor caminho encontrado
    highlight_shortest_path(G, pos, caminho, f"Grafo - Menor caminho: {origem} → {destino} (destacado em vermelho)", "grafo_menor_caminho")

    # 3) Imprime todos os menores caminhos a partir de Lago Norte
    all_shortest_paths_from(G, "Lago Norte")

    # 4) TSP (aproximação) para todos os nós e impressão do resultado
    tsp_ciclo, tsp_custo = tsp_approx(G, nodes=list(G.nodes), cycle=True)
    print(f"\nCaminho mais econômico (TSP): {tsp_ciclo} com custo {tsp_custo}")

    # 5) Exemplo de conversão de custo para valor monetário (multiplica custo por 20)
    tsp_espl, tsp_espl_custo = tsp_approx(G, nodes=list(G.nodes), cycle=True)
    valor_total = tsp_espl_custo * 20
    print(f"\nSaindo da Esplanada, custo total = {tsp_espl_custo}, valor em reais = R${valor_total:.2f}")

if __name__ == "__main__":
    main()
