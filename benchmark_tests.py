# benchmark_suite.py
import random
import time
import matplotlib.pyplot as plt
import numpy as np
import pickle
import string

from main import turouist_problem

def generate_graph(num_nodes, connectivity=0.1, num_cities=5, weight_range=(10, 100), seed=None):
    
    if seed is not None:
        random.seed(seed)
        
    # City codes: 'A', 'B', 'C', ...
    CITY_CODES = list(string.ascii_uppercase[:num_cities])
    
    # Assign cities cyclically
    cities = [CITY_CODES[i % num_cities] for i in range(num_nodes)]
    stations = [(f"st{i+1}", cities[i]) for i in range(num_nodes)]
    
    # Build index map
    idx = {f"{name}-{city}": i for i, (name, city) in enumerate(stations)}
    
    # Generate edges
    edges = []
    for u in range(num_nodes):
        for v in range(num_nodes):
            if u == v:
                continue
            if random.random() < connectivity:
                w = random.randint(weight_range[0], weight_range[1])
                edges.append((u, v, w))
    
    # Pick the first station as source
    source = f"st1-{cities[0]}"
    
    return stations, edges, idx, source

def run_benchmark(sizes, repetitions=3, connectivity_range=(0.05, 0.2), seed=None):
    if seed is not None:
        random.seed(seed)
    
    results = {size: [] for size in sizes}
    
    for size in sizes:
        print(f"Testing size: {size} nodes")
        for rep in range(repetitions):
            # Vary connectivity slightly for diversity
            connectivity = random.uniform(connectivity_range[0], connectivity_range[1])
            num_cities = min(10, max(3, size // 20))  # Scale city count with graph size
            
            # Generate problem instance
            stations, edges, idx, src = generate_graph(
                num_nodes=size,
                connectivity=connectivity,
                num_cities=num_cities,
                weight_range=(10, 100),
                seed=seed + rep if seed else None
            )
            
            # Measure execution time
            start_time = time.time()
            turouist_problem(stations, edges, idx, src)
            elapsed = time.time() - start_time
            
            results[size].append(elapsed)
            print(f"  Repetition {rep+1}/{repetitions}: {elapsed:.6f} seconds")
    
    # Calculate average times
    avg_results = {size: np.mean(times) for size, times in results.items()}
    return avg_results, results

def run_connectivity_benchmark(
    fixed_size=500, 
    connectivity_values=None, 
    repetitions=3,
    num_cities=10,
    seed=None
):
    if seed is not None:
        random.seed(seed)

    max_edge_count = fixed_size * (fixed_size - 1) / 2
    
    results = {conn: [] for conn in connectivity_values}
    edge_counts = {conn: [] for conn in connectivity_values}
    
    print(f"Testing fixed vertex size: {fixed_size} with varying connectivity")
    
    for conn in connectivity_values:
        print(f"\nConnectivity: {conn:.4f}")
        for rep in range(repetitions):
            # Generate problem instance
            stations, edges, idx, src = generate_graph(
                num_nodes=fixed_size,
                connectivity=conn,
                num_cities=num_cities,
                weight_range=(10, 100),
                seed=seed + rep if seed else None
            )
            
            # Measure execution time
            start_time = time.time()
            turouist_problem(stations, edges, idx, src)
            elapsed = time.time() - start_time
            
            results[conn].append(elapsed)
            print(f"  Repetition {rep+1}/{repetitions}: {elapsed:.4f} seconds, {len(edges)} edges")
    
            # Track number of edges
            edge_counts[conn].append(len(edges))
    
    # Calculate average times and edge counts
    avg_results = {size*max_edge_count: np.mean(times) for size, times in results.items()}
    
    return avg_results, results


def save_results(results, filename="benchmark_results.pkl"):
    """Save benchmark results to file"""
    with open(filename, 'wb') as f:
        pickle.dump(results, f)
    print(f"Results saved to {filename}")

def load_results(filename="benchmark_results.pkl"):
    """Load benchmark results from file"""
    with open(filename, 'rb') as f:
        return pickle.load(f)

def size_benchmark():
    # Define problem sizes to test - at least 5 different sizes as requested
    # Creating 10 different sizes for better curve fitting
    sizes = [
        # Small instances (seconds)
        10, 20, 30, 50, 70,
        # Medium instances (minutes)
        100, 150, 200, 300, 400,
        # Large instances (potentially hours for very large graphs)
        500, 700, 900, 1200, 1500
    ]
    
    # Define number of instances per size (at least 50 total instances)
    repetitions_per_size = 4  # 15 sizes * 4 repetitions = 60 total instances
    
    # Run benchmarks
    print(f"Running benchmark suite with {len(sizes)} sizes, {repetitions_per_size} repetitions per size")
    print(f"Total instances: {len(sizes) * repetitions_per_size}")
    
    avg_results, raw_results = run_benchmark(
        sizes=sizes,
        repetitions=repetitions_per_size,
        connectivity_range=(0.05, 0.20),
        seed=42
    )
    
    # Save results
    save_results((avg_results, raw_results))
    
    print("\nBenchmark complete. Results saved as benchmark_results.pkl and benchmark_results.png")

def connectivity_benchmark():
     # Fixed vertex size
    FIXED_SIZE = 1200
    
    # Define connectivity values to test (at least 10 different values)
    connectivity_values = [
        0.01, 0.02, 0.03, 0.05, 0.07,  # Sparse graphs
        0.1, 0.15, 0.2, 0.25, 0.3,     # Medium density
        0.4, 0.5, 0.6, 0.7, 0.8        # Dense graphs
    ]
    
    # Number of repetitions per connectivity value
    repetitions_per_conn = 4  # 15 connectivity values * 4 repetitions = 60 total instances
    
    # Run benchmarks
    print(f"Running connectivity benchmark suite with fixed vertex size {FIXED_SIZE}")
    print(f"Testing {len(connectivity_values)} connectivity values with {repetitions_per_conn} repetitions each")
    print(f"Total instances: {len(connectivity_values) * repetitions_per_conn}")
    
    # Run the benchmarks
    avg_results, raw_results= run_connectivity_benchmark(
        fixed_size=FIXED_SIZE,
        connectivity_values=connectivity_values,
        repetitions=repetitions_per_conn,
        num_cities=10,
        seed=42
    )
    
    # Save results
    save_results((avg_results, raw_results),filename="connectivity_benchmark_results.pkl")
    
    print("\nConnectivity benchmark complete.")
    print("Results saved as connectivity_benchmark_results.pkl")
    print("Plots saved as connectivity_benchmark.png")

if __name__ == "__main__":
    connectivity_benchmark()