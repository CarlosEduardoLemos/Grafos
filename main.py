import networkx as nx
import matplotlib.pyplot as plt

# 1. Criando o grafo dos pontos de entrega
locais_entrega = [
    "Asa Norte", "Asa Sul", "Lago Sul", "Esplanada", "Lago Norte", "Vila Planalto"
]
G = nx.Graph()
G.add_nodes_from(locais_entrega)

# 2. Adicionando as arestas com os respectivos custos (distâncias)
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

# 3. Desenhando o grafo para visualização
pos = nx.spring_layout(G, seed=42)  # Layout fixo para facilitar leitura
plt.figure(figsize=(8, 6))
nx.draw(
    G, pos,
    with_labels=True,
    node_size=2000,
    node_color="lightblue",
    font_size=10,
    font_weight="bold"
)
# Adiciona os custos nas arestas
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
plt.title("Grafo - Pontos de Entrega de Carlos")
plt.show()

# 4. Menor caminho entre Lago Norte e Lago Sul usando Dijkstra
menor_caminho = nx.dijkstra_path(G, source="Lago Norte", target="Lago Sul", weight="weight")
custo_menor_caminho = nx.dijkstra_path_length(G, source="Lago Norte", target="Lago Sul", weight="weight")
print(f"Menor caminho Lago Norte -> Lago Sul: {menor_caminho} com custo {custo_menor_caminho}")

# 5. Custo mínimo para sair do Lago Norte até todos os pontos
print("\nCaminhos mínimos a partir do Lago Norte:")
for destino in locais_entrega:
    caminho = nx.dijkstra_path(G, source="Lago Norte", target=destino, weight="weight")
    custo = nx.dijkstra_path_length(G, source="Lago Norte", target=destino, weight="weight")
    print(f"Lago Norte -> {destino}: caminho {caminho}, custo {custo}")

# 6. Caminho mais econômico para visitar todos os pontos (aproximação do Caixeiro Viajante)
tsp_ciclo = nx.approximation.traveling_salesman_problem(G, weight="weight", cycle=True)
tsp_custo = sum(G[tsp_ciclo[i]][tsp_ciclo[i+1]]['weight'] for i in range(len(tsp_ciclo)-1))
print(f"\nCaminho mais econômico (TSP): {tsp_ciclo} com custo {tsp_custo}")

# 7. Cálculo do gasto em reais (R$20 por unidade de custo)
# Exemplo: partindo da Esplanada e visitando todos os pontos
tsp_esplanada = nx.approximation.traveling_salesman_problem(G, nodes=locais_entrega, cycle=True)
tsp_esplanada_custo = sum(G[tsp_esplanada[i]][tsp_esplanada[i+1]]['weight'] for i in range(len(tsp_esplanada)-1))
valor_total = tsp_esplanada_custo * 20
print(f"\nSaindo da Esplanada, custo total = {tsp_esplanada_custo}, valor em reais = R${valor_total:.2f}")
