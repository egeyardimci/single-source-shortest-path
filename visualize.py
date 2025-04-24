import networkx as nx
import matplotlib.pyplot as plt

def visualize_graph(stations, edges):
    """
    Visualize a directed weighted graph with edge lengths proportional to travel times.

    Args:
        stations: List of station names.
        edges: List of tuples (u, v, w) where u, v are indices into stations, and w is the travel time.
    """
    G = nx.DiGraph()
    # Add nodes
    for name in stations:
        G.add_node(name)
    # Add weighted edges with inverted weights for spring layout
    for u, v, w in edges:
        # 'weight' retained for label, 'spring_weight' used for layout
        G.add_edge(stations[u], stations[v], weight=w, spring_weight=1.0 / w)

    # Compute layout: stronger springs (smaller times) pull nodes closer
    pos = nx.spring_layout(G, weight='spring_weight', iterations=100)

    # Draw the graph
    nx.draw(G, pos, with_labels=True, arrows=True)
    # Draw weights on edges
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    plt.title("Tourist Problem Graph (Edge Lengths ∝ Travel Time)")
    plt.axis('off')
    plt.show()