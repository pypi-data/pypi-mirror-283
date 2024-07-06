import numpy as np
from PyRandomLoop.core.rpm import RPM  # Import your RPM class
import time


def benchmark_method(method):
    """Benchmark a single method."""
    start_time = time.time()
    out = method()
    end_time = time.time()
    return end_time - start_time

def benchmark():
    
    # Initialize the RPM instance
    m = RPM(3, 64, 2)
    m.random_init()
    # List of methods to benchmark with their arguments and keyword arguments
    methods_to_benchmark = [
        (m.loop_builder, [], {}),
        (m.mean_links, [], {}),
        (m.mean_local_time, [], {}),
        (m.mean_local_time, [], {}),
        (m.compute_corr, [], {}) 
    ]
    
    # Benchmark each method
    print("### Time per call for each method ###\n")
    for method, args, kwargs in methods_to_benchmark:
        time_per_call = benchmark_method(method) * 1000
        print(f"{method.__name__:20} {time_per_call:.2f} ms")
        
    # Benchmark number of steps/s for the `run` method using time library
    def benchmark_run_steps(m, steps):
        start_time = time.time()
        m.step(steps, progress_bar=False)
        end_time = time.time()
        return end_time - start_time

    # Benchmark the step method with 1,000,000 steps
    elapsed_time = benchmark_run_steps(m, 1_000_000)
    
    steps_per_second = 1_000_000 / elapsed_time
    print("\n##################################################\n")
    
    print(f"Steps per second: {steps_per_second:.2f} steps/s\n")


def main():
    benchmark()

if __name__ == '__main__':
    main()
