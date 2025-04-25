import networkx as nx
import matplotlib.pyplot as plt

def visualize_graph(stations, edges):
    G = nx.DiGraph()
    # Add nodes
    for name in stations:
        G.add_node(name)
    # Add weighted edges with inverted weights for spring layout
    for u, v, w in edges:
        # 'weight' retained for label, 'spring_weight' used for layout
        if(w == 0):
            w = 1e-10
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