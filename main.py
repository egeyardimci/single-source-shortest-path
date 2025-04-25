import math
import time
import correctness_tests
from visualize import visualize_graph

def turouist_problem(stations, edges, idx, source):
    n = len(stations)
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
            if memo[k-1][u] + w < memo[k][v]:
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
            print(f"\nShortest travel time to {city} from {source}: {travel_time} minutes")
            print(f"Route: {' -> '.join([item for item in route if isinstance(item, str)])}")
            print(f"Segment times: {[item for item in route if isinstance(item, int)]}")

if __name__ == "__main__":
    stations, edges, idx, source = correctness_tests.test_9()
    turouist_problem(stations, edges, idx, source)
    visualize_graph(stations,edges)