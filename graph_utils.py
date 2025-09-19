import networkx as nx
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple, Optional

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

def validate_nodes(G: nx.Graph, nodes: List[str]) -> bool:
    missing = [node for node in nodes if node not in G.nodes]
    return not missing
