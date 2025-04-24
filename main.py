import time
# Define stations and example graph for the tourist problem
stations = ["Harem", "Bostanci", "Merkez", "YHT", "Yeni"]
idx = {name: i for i, name in enumerate(stations)}

# Build directed edge list (u, v, time)
edges = []
# Intra-city transfers
edges += [
    (idx["Harem"],    idx["Bostanci"], 30),
    (idx["Bostanci"], idx["Harem"],   30),
    (idx["YHT"],      idx["Yeni"],     10),
    (idx["Yeni"],     idx["YHT"],      10),
]
# Inter-city travel times (two-way)
edges += [
    (idx["Harem"],    idx["Merkez"],  100),
    (idx["Merkez"],   idx["Harem"],   100),
    (idx["Bostanci"], idx["YHT"],     180),
    (idx["YHT"],      idx["Bostanci"],180),
    (idx["Merkez"],   idx["Yeni"],    120),
    (idx["Yeni"],     idx["Merkez"],  120),
]

n = len(stations)
src = idx["Harem"]

# Recursive DP (Bellman–Ford style) with memoization: f(k, v)
memo = [[None] * n for _ in range(n)]

def f(k, v):
    if memo[k][v] is not None:
        return memo[k][v]
    if k == 0:
        memo[k][v] = 0 if v == src else float('inf')
    else:
        best = f(k-1, v)
        for u2, v2, w in edges:
            if v2 == v:
                cost = f(k-1, u2) + w
                if cost < best:
                    best = cost
        memo[k][v] = best
    return memo[k][v]

# Compute shortest times using up to n−1 edges
target_station = idx["Yeni"]
start_time = time.time()
dist = f(n-1, target_station)
end_time = time.time()
print(f"Time taken: {end_time - start_time:.20f} seconds")

# Display results
print("Shortest travel times from Istanbul-Harem (Harem):")
print(f"To -> {stations[target_station]}: {dist} minutes")

from visualize import visualize_graph
visualize_graph(stations,edges)