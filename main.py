import math
import time
# Define stations and example graph for the tourist problem
stations = [("Harem", "Istanbul"), ("Bostanci","Istanbul"), ("Merkez","Bursa"), ("YHT","Eskisehir"), ("Yeni","Eskisehir")]
idx = {f"{name}-{city}": i for i, (name, city) in enumerate(stations)}

# Build directed edge list (u, v, time)
edges = []
# Intra-city transfers
edges += [
    (idx["Harem-Istanbul"],    idx["Bostanci-Istanbul"], 30),
    (idx["Bostanci-Istanbul"], idx["Harem-Istanbul"],   30),
    (idx["YHT-Eskisehir"],      idx["Yeni-Eskisehir"],     10),
    (idx["Yeni-Eskisehir"],     idx["YHT-Eskisehir"],      10),
]
# Inter-city travel times (two-way)
edges += [
    (idx["Harem-Istanbul"],    idx["Merkez-Bursa"],  100),
    (idx["Merkez-Bursa"],   idx["Harem-Istanbul"],   100),
    (idx["Bostanci-Istanbul"], idx["YHT-Eskisehir"],     180),
    (idx["YHT-Eskisehir"],      idx["Bostanci-Istanbul"],180),
    (idx["Merkez-Bursa"],   idx["Yeni-Eskisehir"],    120),
    (idx["Yeni-Eskisehir"],     idx["Merkez-Bursa"],  120),
]

n = len(stations)
source = "Harem-Istanbul"
src = idx[source]

preds = [[] for _ in range(n)]

# Recursive DP (Bellman–Ford style) with memoization: f(k, v)
memo = [[None] * n for _ in range(n)]

def bellman_ford_recursive(k, edges, n, src):
    if k == 0:
        for i in range(n):
            memo[k][i] = math.inf
            memo[k][src] = 0
        return
        
    bellman_ford_recursive(k-1, edges, n, src)
    
    memo[k] = memo[k-1][:]  # Copy previous distances
    
    for u, v, w in edges:
        if memo[k-1][u] + w < memo[k-1][v]:
            memo[k][v] = memo[k-1][u] + w
            preds[v] = (stations[u],w)
    
    return memo[n-1]

start_time = time.time()
dist = bellman_ford_recursive(n-1, edges, n, src)
end_time = time.time()
print(f"Time taken: {end_time - start_time:.20f} seconds")

def trace_route(station):
    path = []
    station = (station,0)
    # Backtrack to find the path from the source to the station
    while station is not None:
        station_weight = station[1]
        station_name = f"{station[0][0]}-{station[0][1]}"
        if(station_weight != 0):
            path.append(station_weight)
        path.append(station_name)
        station = preds[idx[station_name]] if preds[idx[station_name]] else None
    return list(reversed(path))

cities = set(station[1] for station in stations)
for city in cities:
    if city == source.split("-")[1]:
        continue
    # Find stations in the current city with the shortest travel time
    city_stations = [stations[i] for i in range(len(stations)) if stations[i][1] == city]
    city_distances = [dist[idx[f"{station[0]}-{station[1]}"]] for station in city_stations]
    
    if city_distances:
        # Find the station with minimum distance
        min_distance_idx = city_distances.index(min(city_distances))
        best_station = city_stations[min_distance_idx]
        best_station_idx = idx[f"{best_station[0]}-{best_station[1]}"]
        
        # Get the travel time and route
        travel_time = dist[best_station_idx]
        route = trace_route(best_station)
        
        # Print the results
        print(f"\nShortest travel time to {city}: {travel_time} minutes")
        print(f"Route: {' -> '.join([item for item in route if isinstance(item, str)])}")
        print(f"Segment times: {[item for item in route if isinstance(item, int)]}")

from visualize import visualize_graph
visualize_graph(stations, edges)