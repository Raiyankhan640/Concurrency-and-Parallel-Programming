import concurrent.futures
import time
import random
import threading

# Assignment Part 4: Thread Pool for Parallel Tasks
# This program demonstrates the benefits of using a thread pool for parallel execution
# by comparing sequential processing vs parallel processing timings.

def process_task(task_id):
    """Simulate a CPU-bound or I/O-bound task"""
    thread_name = threading.current_thread().name
    print(f"Task {task_id} starting on thread {thread_name}")
    
    # Simulate work (sleep)
    time.sleep(1.0) 
    
    print(f"Task {task_id} completed")
    return task_id

if __name__ == "__main__":
    print("--- Part 4: Sequential vs Parallel Execution with ThreadPool ---")
    
    num_tasks = 10
    
    # --- Sequential Execution ---
    print("\nStarting Sequential Execution...")
    start_time = time.time()
    
    for i in range(num_tasks):
        process_task(i)
        
    sequential_time = time.time() - start_time
    print(f"Sequential Execution Time: {sequential_time:.2f} seconds")


    # --- Parallel Execution ---
    print("\nStarting Parallel Execution (4 workers)...")
    start_time = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        # Submit tasks
        results = executor.map(process_task, range(num_tasks))
        
        # Iterate over results (this waits for all to complete if not already)
        for _ in results:
            pass

    parallel_time = time.time() - start_time
    print(f"Parallel Execution Time: {parallel_time:.2f} seconds")

    # --- Comparison ---
    print("\n--- Results ---")
    print(f"Sequential: {sequential_time:.2f}s")
    print(f"Parallel:   {parallel_time:.2f}s")
    if parallel_time > 0:
        speedup = sequential_time / parallel_time
        print(f"Speedup:    {speedup:.2f}x")
    else:
        print("Speedup:    Infinite (Parallel time was 0)")
