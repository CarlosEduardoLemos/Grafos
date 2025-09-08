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
    ("Asa Norte", "Asa Sul", 12),
    ("Asa Norte", "Esplanada", 6),
    ("Asa Norte", "Lago Norte", 11),
    ("Asa Sul", "Esplanada", 5),
    ("Asa Sul", "Lago Sul", 7),
    ("Esplanada", "Lago Sul", 14),
    ("Esplanada", "Vila Planalto", 10),
    ("Lago Norte", "Vila Planalto", 5),
    ("Lago Norte", "Lago Sul", 8),
    ("Lago Sul", "Vila Planalto", 12),
]
G.add_weighted_edges_from(conexoes)

"""
------------------------------------------------------------
3) Visualização do grafo
- spring_layout: posicionamento automático dos nós (seed fixo para reprodutibilidade)
- nx.draw: desenha nós e rótulos
- nx.draw_networkx_edge_labels: mostra os pesos das arestas (custos/distâncias)
"""
pos = nx.spring_layout(G, seed=42)  # layout determinístico
plt.figure(figsize=(8, 6))
nx.draw(
    G, pos,
    with_labels=True,
    node_size=2000,
    node_color="lightblue",
    font_size=10,
    font_weight="bold"
)
# Obtém os pesos para rotular as arestas
labels = nx.get_edge_attributes(G, 'weight')  # dicionário {(u,v): peso}
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
plt.title("Grafo - Pontos de Entrega de Carlos")
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
