import networkx as nx
import matplotlib.pyplot as plt

# Criando o grafo
G = nx.Graph()

# Adicionando os vértices (locais de entrega)
vertices = ["Asa Norte", "Asa Sul", "Lago Sul", "Esplanada", "Lago Norte", "Vila Planalto"]
G.add_nodes_from(vertices)

# Adicionando as arestas com os respectivos custos
arestas = [
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

G.add_weighted_edges_from(arestas)

# Desenhar o grafo
pos = nx.spring_layout(G, seed=42)  # Layout para manter o desenho estável
plt.figure(figsize=(8, 6))
nx.draw(G, pos, with_labels=True, node_size=2000, node_color="lightblue", font_size=10, font_weight="bold")
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
plt.title("Grafo - Pontos de Entrega de Carlos")
plt.show()

# 1. Menor caminho do Lago Norte até Lago Sul
shortest_path = nx.dijkstra_path(G, source="Lago Norte", target="Lago Sul", weight="weight")
shortest_cost = nx.dijkstra_path_length(G, source="Lago Norte", target="Lago Sul", weight="weight")
print(f"Menor caminho Lago Norte -> Lago Sul: {shortest_path} com custo {shortest_cost}")

# 2. Custo para sair do Lago Norte até todos os pontos
for destino in vertices:
    path = nx.dijkstra_path(G, source="Lago Norte", target=destino, weight="weight")
    cost = nx.dijkstra_path_length(G, source="Lago Norte", target=destino, weight="weight")
    print(f"Lago Norte -> {destino}: caminho {path}, custo {cost}")

# 3. Caminho mais econômico para visitar todos os pontos (aproximação do Caixeiro Viajante)
tsp_path = nx.approximation.traveling_salesman_problem(G, weight="weight", cycle=True)
tsp_cost = sum(G[tsp_path[i]][tsp_path[i+1]]['weight'] for i in range(len(tsp_path)-1))
print(f"Caminho mais econômico (TSP): {tsp_path} com custo {tsp_cost}")

# 4. Cálculo do gasto em reais (R$20 por unidade de custo)
esplanada_path = nx.approximation.traveling_salesman_problem(G, nodes=vertices, cycle=True)
esplanada_cost = sum(G[esplanada_path[i]][esplanada_path[i+1]]['weight'] for i in range(len(esplanada_path)-1))
valor_reais = esplanada_cost * 20
print(f"Saindo da Esplanada, custo total = {esplanada_cost}, valor em reais = R${valor_reais:.2f}")
