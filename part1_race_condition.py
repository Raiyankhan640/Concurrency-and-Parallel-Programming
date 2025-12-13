import threading
import time

"""
Race Condition and Basic Synchronization Demo
This module demonstrates a classic concurrency issue where multiple threads
access shared data without synchronization, leading to incorrect results.
It then shows how a simple lock mechanism ensures thread safety.
"""

class Counter:
    """
    A shared counter that can be incremented by multiple threads.
    
    Attributes:
        value (int): The current counter value.
        use_lock (bool): Flag to enable/disable locking mechanism.
        lock (threading.Lock): Lock object for synchronization.
    """
    def __init__(self, use_lock=False):
        self.value = 0
        self.use_lock = use_lock
        self.lock = threading.Lock() if use_lock else None

    def increment(self):
        """
        Increment the counter by one.
        If use_lock is True, the operation is thread-safe.
        """
        if self.use_lock:
            with self.lock:
                self._increment_logic()
        else:
            self._increment_logic()

    def _increment_logic(self):
        """
        Core increment logic that simulates a race condition.
        A short sleep is introduced to increase the chance of context switching.
        """
        temp = self.value          # Read current value
        time.sleep(0.0001)         # Simulate processing delay
        temp = temp + 1            # Increment local copy
        self.value = temp          # Write back to shared variable


def run_simulation(use_lock, num_threads=3, increments_per_thread=1000):
    """
    Run a simulation with multiple threads incrementing a shared counter.
    
    Args:
        use_lock (bool): Whether to use locking for synchronization.
        num_threads (int): Number of threads to spawn.
        increments_per_thread (int): Number of increments per thread.
    
    Returns:
        int: Final counter value after all threads complete.
    """
    counter = Counter(use_lock=use_lock)
    threads = []
    
    # Create and start threads
    for _ in range(num_threads):
        t = threading.Thread(
            target=lambda: [counter.increment() for _ in range(increments_per_thread)]
        )
        threads.append(t)
        t.start()
    
    # Wait for all threads to finish
    for t in threads:
        t.join()
        
    return counter.value


if __name__ == "__main__":
    print("=== Race Condition vs. Synchronization Demo ===\n")
    
    num_threads = 3
    increments_per_thread = 1000
    expected = num_threads * increments_per_thread
    
    # Run WITHOUT synchronization
    print("Running WITHOUT lock (UNSAFE):")
    result_without = run_simulation(
        use_lock=False,
        num_threads=num_threads,
        increments_per_thread=increments_per_thread
    )
    print(f"  Expected final value: {expected}")
    print(f"  Actual final value:   {result_without}")
    if result_without != expected:
        print("  RACE CONDITION DETECTED: Result is incorrect")
    else:
        print("  Note: Result may occasionally be correct due to scheduler luck, but the code is unsafe.\n")
    
    # Run WITH synchronization
    print("Running WITH lock (THREAD-SAFE):")
    result_with = run_simulation(
        use_lock=True,
        num_threads=num_threads,
        increments_per_thread=increments_per_thread
    )
    print(f"  Expected final value: {expected}")
    print(f"  Actual final value:   {result_with}")
    if result_with == expected:
        print("  Lock prevented race condition, result is correct.")
    else:
        print("  Unexpected error occurred.")