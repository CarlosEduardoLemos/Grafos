import networkx as nx
import matplotlib.pyplot as plt

"""
------------------------------------------------------------
1) Definição dos pontos (vértices) do problema
lista com os nomes dos locais de entrega (cada nome => um nó no grafo)
"""
locais_entrega = [
    "Asa Norte", "Asa Sul", "Lago Sul", "Esplanada", "Lago Norte", "Vila Planalto"
]

# Cria um grafo não direcionado (cada aresta representa ligação entre locais)
G = nx.Graph()
G.add_nodes_from(locais_entrega)  # adiciona os nós ao grafo

"""
------------------------------------------------------------
2) Arestas com pesos (custos/distâncias)
Cada tupla é (origem, destino, peso). Usamos add_weighted_edges_from para
armazenar o peso na propriedade 'weight' da aresta.
"""
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
G.add_weighted_edges_from(conexoes)

"""
------------------------------------------------------------
3) Visualização do grafo
- spring_layout: posicionamento automático dos nós (seed fixo para reprodutibilidade)
- nx.draw: desenha nós e rótulos
- nx.draw_networkx_edge_labels: mostra os pesos das arestas (custos/distâncias)
"""
# pos = nx.spring_layout(G, seed=42)  # layout determinístico
# Substitui layout automático por posições manuais para reproduzir a figura fornecida
pos = {
    "Asa Norte": (-1.0,  0.0),
    "Asa Sul":   (-0.6,  0.9),
    "Lago Sul":  ( 0.6,  0.9),
    "Vila Planalto": ( 1.0,  0.0),
    "Lago Norte": ( 0.0, -0.9),
    "Esplanada":  ( 0.0,  0.15),
}

# Figura principal: grafo completo no estilo da imagem
plt.figure(figsize=(8, 6))
nx.draw_networkx_nodes(
    G, pos,
    node_size=2500,
    node_color="white",
    edgecolors="black",
    linewidths=2
)
nx.draw_networkx_labels(
    G, pos,
    font_size=12,
    font_weight="bold"
)
# arestas em azul claro como na imagem
nx.draw_networkx_edges(G, pos, edge_color="tab:blue", width=2)
# rótulos das arestas em azul
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_color="tab:blue", font_size=10)

# legenda / legenda inferior similar à figura
plt.title("Grafo - Pontos de Entrega de Carlos", fontsize=14)
plt.figtext(0.5, 0.01, "Figura 1 - Grafo representando os pontos de entrega de Carlos", ha="center", fontsize=9, style="italic")
plt.axis('off')
plt.tight_layout()
plt.show()

"""
------------------------------------------------------------
4) Menor caminho entre dois pontos (Dijkstra)
nx.dijkstra_path retorna a sequência de nós do caminho mínimo considerando 'weight'
nx.dijkstra_path_length retorna o custo total (soma dos pesos) do caminho
"""
menor_caminho = nx.dijkstra_path(G, source="Lago Norte", target="Lago Sul", weight="weight")
custo_menor_caminho = nx.dijkstra_path_length(G, source="Lago Norte", target="Lago Sul", weight="weight")
print(f"Menor caminho Lago Norte -> Lago Sul: {menor_caminho} com custo {custo_menor_caminho}")

# === Nova tela: visualiza o grafo e destaca o menor caminho Lago Norte -> Lago Sul ===
# caminho já calculado em `menor_caminho`
path_edges = list(zip(menor_caminho, menor_caminho[1:]))

plt.figure(figsize=(8, 6))
# desenha grafo base (arestas mais claras)
nx.draw_networkx_nodes(
    G, pos,
    node_size=2500,
    node_color="white",
    edgecolors="black",
    linewidths=2
)
nx.draw_networkx_labels(G, pos, font_size=12, font_weight="bold")
nx.draw_networkx_edges(G, pos, edge_color="lightgray", width=2)

# rótulos das arestas em azul (mantém leitura)
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_color="tab:blue", font_size=10)

# destaca arestas do caminho mínimo em vermelho e mais espessas
nx.draw_networkx_edges(G, pos, edgelist=path_edges, width=4, edge_color="red")
# destaca nós do caminho mínimo em vermelho (com borda preta)
nx.draw_networkx_nodes(G, pos, nodelist=menor_caminho, node_color="red", edgecolors="black", node_size=2500, linewidths=2)

plt.title("Grafo - Menor caminho: Lago Norte → Lago Sul (destacado em vermelho)", fontsize=14)
plt.axis('off')
plt.tight_layout()
plt.show()

"""
------------------------------------------------------------
5) Menores caminhos a partir de um nó para todos os demais
Itera por cada destino e calcula caminho mínimo e custo a partir de "Lago Norte"
"""
print("\nCaminhos mínimos a partir do Lago Norte:")
for destino in locais_entrega:
    caminho = nx.dijkstra_path(G, source="Lago Norte", target=destino, weight="weight")
    custo = nx.dijkstra_path_length(G, source="Lago Norte", target=destino, weight="weight")
    # Exibe o caminho (sequência de nós) e o custo total (soma dos pesos)
    print(f"Lago Norte -> {destino}: caminho {caminho}, custo {custo}")

"""
------------------------------------------------------------
6) Aproximação do Caixeiro Viajante (TSP)
nx.approximation.traveling_salesman_problem retorna uma rota aproximada que visita
todos os nós. Parâmetro cycle=True pede que retorne um ciclo (volta ao ponto inicial).
Note: é uma heurística / aproximação, não garante solução ótima exata para todos os grafos.
"""
tsp_ciclo = nx.approximation.traveling_salesman_problem(G, weight="weight", cycle=True)
# Calcula custo somando os pesos das arestas sucessivas do ciclo retornado
tsp_custo = sum(G[tsp_ciclo[i]][tsp_ciclo[i+1]]['weight'] for i in range(len(tsp_ciclo)-1))
print(f"\nCaminho mais econômico (TSP): {tsp_ciclo} com custo {tsp_custo}")

"""
------------------------------------------------------------
7) Exemplo de cálculo do custo monetário
Supondo R$20 por unidade de distância/custo: multiplica-se o custo total do TSP por 20.
Ao chamar traveling_salesman_problem com nodes=locais_entrega garantimos que a rota
considere exatamente o conjunto de nós desejado.
"""
tsp_esplanada = nx.approximation.traveling_salesman_problem(G, nodes=locais_entrega, cycle=True)
tsp_esplanada_custo = sum(G[tsp_esplanada[i]][tsp_esplanada[i+1]]['weight'] for i in range(len(tsp_esplanada)-1))
valor_total = tsp_esplanada_custo * 20  # valor em reais (R$20 por unidade de custo)
print(f"\nSaindo da Esplanada, custo total = {tsp_esplanada_custo}, valor em reais = R${valor_total:.2f}")
