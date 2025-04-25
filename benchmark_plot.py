import pickle

def plot_benchmark_results(avg_results):
    import matplotlib.pyplot as plt
    import numpy as np

    # Extract sizes and times in sorted order
    sizes = sorted(avg_results.keys())
    times = [avg_results[size] for size in sizes]

    plt.figure(figsize=(10, 6))

    # Plot average times with connected line
    plt.plot(sizes, times, 'o-', color='blue', linewidth=2, 
                markersize=8, label="Average execution time")

    # Add best-fit lines for common complexity classes
    x = np.array(sizes)

    # Set logarithmic scales for both axes
    plt.xscale('log')
    plt.yscale('log')

    # Add labels and styling
    plt.title("Algorithm Performance Benchmark (Log Scale)", fontsize=16)
    plt.xlabel("Problem Size (Number of Nodes)", fontsize=14)
    plt.ylabel("Execution Time (seconds)", fontsize=14)
    plt.grid(True, alpha=0.3, which='both')  # Grid lines for both major and minor ticks
    plt.legend(fontsize=12)

    plt.tight_layout()

    # Save plot
    plt.savefig("benchmark_log_results.png", dpi=300)
    plt.show()

def load_results(filename="benchmark_results.pkl"):
    """Load benchmark results from file"""
    with open(filename, 'rb') as f:
        return pickle.load(f)
# Example usage:
avg_results, results = load_results("benchmark_results.pkl")
plot_benchmark_results(avg_results)