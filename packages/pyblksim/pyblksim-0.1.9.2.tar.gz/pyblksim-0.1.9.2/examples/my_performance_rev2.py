import time
import importlib
from memory_profiler import memory_usage

#script_names = ['example_2_sources_scope_file', 'example_3_spectrum_analysis', 'example_4_ook_modulation_demodulation']  # List the names of your Python script modules here

## for comparing the performance between bdsim and pyblksim.
#script_names = ['bdsim_performance_eval_example', 'pyblksim_performance_eval_example' ]  # List the names of your Python script modules here
script_names = ['pyblksim_performance_eval_example']  # List the names of your Python script modules here
    
    
def load_and_run_example(script_name):
    # Dynamically import the example script module
    script_module = importlib.import_module(script_name)
    # Assuming each script has a main function or similar entry point
    if hasattr(script_module, 'main'):
        script_module.main()

def measure_performance(script_name):
    # Measure start time
    start_time = time.time()

    # Profile memory usage
    # The interval and timeout are important to get more accurate results depending on the execution time of your script
    mem_usage = memory_usage(lambda: load_and_run_example(script_name), interval=0.1, timeout=None, include_children=True)

    # Measure end time
    end_time = time.time()

    # Calculate execution time and peak memory usage
    execution_time = end_time - start_time
    peak_memory = max(mem_usage)
    return execution_time, peak_memory

if __name__ == "__main__":
    num_runs = 2
    results = {}

    for script_name in script_names:
        total_time = 0
        total_peak_memory = 0

        for i in range(num_runs):
            exec_time, peak_mem = measure_performance(script_name)
            total_time += exec_time
            total_peak_memory += peak_mem

        average_time = total_time / num_runs
        average_peak_memory = total_peak_memory / num_runs

        results[script_name] = (average_time, average_peak_memory)

        # Output total and average results for each script
        print(f"\n{script_name}:")
        print(f"Total execution time for {num_runs} runs: {total_time} seconds")
        print(f"Total peak memory usage for {num_runs} runs: {total_peak_memory} MiB")
        print(f"Average execution time: {average_time} seconds")
        print(f"Average peak memory usage: {average_peak_memory} MiB\n")
