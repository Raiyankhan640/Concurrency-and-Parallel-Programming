"""
Thread Pool Executor Demonstration
This module compares sequential vs parallel task execution using Python's
ThreadPoolExecutor. It demonstrates the performance benefits of parallelization
for I/O-bound operations and shows thread reuse patterns.
"""

import concurrent.futures
import time
import random
import threading
import math
from datetime import datetime


class TaskProcessor:
    """
    A class to demonstrate different types of tasks that can be parallelized
    using a thread pool.
    """
    
    def __init__(self):
        self.execution_log = []
    
    def fibonacci_task(self, n):
        """
        CPU-bound task: Calculate nth Fibonacci number (simplified for demo).
        
        Args:
            n (int): Fibonacci sequence position to calculate.
        
        Returns:
            tuple: Task ID and result.
        """
        task_id = f"Fibonacci({n})"
        thread_name = threading.current_thread().name
        start_time = time.time()
        
        print(f"[{thread_name}] Starting {task_id} at {datetime.now().strftime('%H:%M:%S')}")
        
        # Simplified Fibonacci calculation (not optimal for large n)
        if n <= 1:
            result = n
        else:
            a, b = 0, 1
            for _ in range(2, n + 1):
                a, b = b, a + b
            result = b
        
        # Simulate additional processing
        time.sleep(random.uniform(0.3, 0.7))
        
        end_time = time.time()
        duration = end_time - start_time
        
        log_entry = {
            'task': task_id,
            'thread': thread_name,
            'result': result,
            'duration': duration
        }
        self.execution_log.append(log_entry)
        
        print(f"[{thread_name}] Completed {task_id}: Fibonacci({n}) = {result} (took {duration:.2f}s)")
        return result
    
    def io_bound_task(self, task_id):
        """
        I/O-bound task: Simulates file/network operations with sleep.
        
        Args:
            task_id (int): Unique task identifier.
        
        Returns:
            tuple: Task ID and completion status.
        """
        thread_name = threading.current_thread().name
        task_name = f"I/O-Task-{task_id}"
        start_time = time.time()
        
        print(f"[{thread_name}] Starting {task_name} at {datetime.now().strftime('%H:%M:%S')}")
        
        # Simulate I/O operations with varying sleep times
        operation_time = random.uniform(0.5, 2.0)
        time.sleep(operation_time)
        
        end_time = time.time()
        duration = end_time - start_time
        
        log_entry = {
            'task': task_name,
            'thread': thread_name,
            'result': 'SUCCESS',
            'duration': duration
        }
        self.execution_log.append(log_entry)
        
        print(f"[{thread_name}] Completed {task_name} (took {duration:.2f}s)")
        return task_id, 'COMPLETED'
    
    def counting_task(self, task_id):
        """
        Mixed CPU/I-O task: Counts with simulated processing delays.
        
        Args:
            task_id (int): Unique task identifier.
        
        Returns:
            tuple: Task ID and count.
        """
        thread_name = threading.current_thread().name
        task_name = f"Count-Task-{task_id}"
        start_time = time.time()
        
        print(f"[{thread_name}] Starting {task_name} at {datetime.now().strftime('%H:%M:%S')}")
        
        # Count operations with occasional delays
        total = 0
        for i in range(1, random.randint(500, 1500)):
            total += i
            if i % 200 == 0:
                time.sleep(0.01)  # Simulate occasional I/O
        
        end_time = time.time()
        duration = end_time - start_time
        
        log_entry = {
            'task': task_name,
            'thread': thread_name,
            'result': f"Sum up to {i} = {total}",
            'duration': duration
        }
        self.execution_log.append(log_entry)
        
        print(f"[{thread_name}] Completed {task_name}: Counted to {i} (took {duration:.2f}s)")
        return task_id, total
    
    def sequential_execution(self, tasks):
        """
        Execute tasks sequentially (one after another).
        
        Args:
            tasks (list): List of task functions and arguments.
        
        Returns:
            float: Total execution time in seconds.
        """
        print("=" * 60)
        print("SEQUENTIAL EXECUTION")
        print("=" * 60)
        
        start_time = time.time()
        
        for i, (task_func, args) in enumerate(tasks):
            task_func(*args if isinstance(args, tuple) else (args,))
        
        sequential_time = time.time() - start_time
        print(f"\nSequential execution completed in {sequential_time:.2f} seconds")
        return sequential_time
    
    def parallel_execution(self, tasks, max_workers=4):
        """
        Execute tasks in parallel using ThreadPoolExecutor.
        
        Args:
            tasks (list): List of task functions and arguments.
            max_workers (int): Maximum number of worker threads.
        
        Returns:
            float: Total execution time in seconds.
        """
        print("\n" + "=" * 60)
        print(f"PARALLEL EXECUTION ({max_workers} worker threads)")
        print("=" * 60)
        
        start_time = time.time()
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all tasks to the thread pool
            futures = []
            for task_func, args in tasks:
                future = executor.submit(task_func, *args if isinstance(args, tuple) else (args,))
                futures.append(future)
            
            # Wait for all tasks to complete and collect results
            results = []
            for future in concurrent.futures.as_completed(futures):
                try:
                    result = future.result(timeout=10)
                    results.append(result)
                except Exception as e:
                    print(f"Task raised an exception: {e}")
        
        parallel_time = time.time() - start_time
        print(f"\nParallel execution completed in {parallel_time:.2f} seconds")
        return parallel_time
    
    def print_summary(self, sequential_time, parallel_time, max_workers):
        """
        Print comparison summary between sequential and parallel execution.
        
        Args:
            sequential_time (float): Time taken for sequential execution.
            parallel_time (float): Time taken for parallel execution.
            max_workers (int): Number of worker threads used.
        """
        print("\n" + "=" * 60)
        print("PERFORMANCE COMPARISON SUMMARY")
        print("=" * 60)
        
        print(f"\nConfiguration:")
        print(f"  Total tasks executed: {len(self.execution_log)}")
        print(f"  Worker threads in pool: {max_workers}")
        
        print(f"\nExecution Times:")
        print(f"  Sequential: {sequential_time:.2f} seconds")
        print(f"  Parallel:   {parallel_time:.2f} seconds")
        
        if parallel_time > 0:
            speedup = sequential_time / parallel_time
            efficiency = (speedup / max_workers) * 100
            print(f"\nPerformance Metrics:")
            print(f"  Speedup: {speedup:.2f}x faster than sequential")
            print(f"  Efficiency: {efficiency:.1f}% of theoretical maximum")
        
        print(f"\nThread Utilization:")
        thread_counts = {}
        for log in self.execution_log:
            thread_name = log['thread']
            thread_counts[thread_name] = thread_counts.get(thread_name, 0) + 1
        
        for thread, count in thread_counts.items():
            print(f"  {thread}: {count} tasks")
    
    def run_comparison(self):
        """
        Run the complete comparison between sequential and parallel execution.
        """
        print("THREAD POOL EXECUTOR DEMONSTRATION")
        print("Comparing Sequential vs Parallel Task Processing")
        print("=" * 60)
        
        # Define 10 different tasks with varied workloads
        tasks = [
            (self.fibonacci_task, 20),
            (self.io_bound_task, 1),
            (self.counting_task, 1),
            (self.fibonacci_task, 15),
            (self.io_bound_task, 2),
            (self.counting_task, 2),
            (self.io_bound_task, 3),
            (self.fibonacci_task, 25),
            (self.counting_task, 3),
            (self.io_bound_task, 4)
        ]
        
        # Run sequential execution
        sequential_time = self.sequential_execution(tasks)
        
        # Clear log for parallel execution
        self.execution_log = []
        
        # Run parallel execution with 4 workers
        max_workers = 4
        parallel_time = self.parallel_execution(tasks, max_workers)
        
        # Print summary comparison
        self.print_summary(sequential_time, parallel_time, max_workers)
        
        print("\n" + "=" * 60)
        print("KEY OBSERVATIONS:")
        print("=" * 60)
        print("1. Parallel execution shows significant speedup for I/O-bound tasks")
        print("2. Thread pool efficiently reuses threads (see thread names in output)")
        print("3. The speedup is less than theoretical maximum due to:")
        print("   - Python's Global Interpreter Lock (GIL) for CPU-bound tasks")
        print("   - Overhead of thread creation and management")
        print("   - Task dependencies and synchronization requirements")
        print("=" * 60)


if __name__ == "__main__":
    """
    Main execution block demonstrating ThreadPoolExecutor benefits.
    
    This program shows:
    1. Different types of tasks (CPU-bound, I/O-bound, mixed)
    2. Sequential execution timing
    3. Parallel execution with thread pool timing
    4. Comparison and analysis of results
    """
    processor = TaskProcessor()
    processor.run_comparison()