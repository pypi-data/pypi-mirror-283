import time
from memory_profiler import memory_usage

def load_and_run_example():
    # Import the example script module if it is a module
    # or define this function to execute its contents
    import example_2_sources_scope_file
    #from test import run_analysis
    #run_analysis()  # Assuming there is a function like this in your script

def measure_performance():
    # Measure start time
    start_time = time.time()

    # Profile memory usage
    # The interval and timeout are important to get more accurate results depending on the execution time of your script
    mem_usage = memory_usage(load_and_run_example, interval=0.1, timeout=None, include_children=True)

    # Measure end time
    end_time = time.time()

    # Calculate execution time and peak memory usage
    execution_time = end_time - start_time
    peak_memory = max(mem_usage)
    return execution_time, peak_memory

if __name__ == "__main__":
    num_runs = 2
    total_time = 0
    total_peak_memory = 0

    for _ in range(num_runs):
        exec_time, peak_mem = measure_performance()
        total_time += exec_time
        total_peak_memory += peak_mem

    average_time = total_time / num_runs
    average_peak_memory = total_peak_memory / num_runs

    # Output average results
    print(f"Average execution time: {average_time} seconds")
    print(f"Average peak memory usage: {average_peak_memory} MiB")
