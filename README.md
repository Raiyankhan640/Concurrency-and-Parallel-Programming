# Concurrency Assignment - [Khan Raiyan Ibne Reza]

## How to Run
This assignment contains 4 independent parts implemented in Python.

1. **Part 1: Race Condition**
   ```bash
   python part1_race_condition.py
   ```
2. **Part 2: Producer-Consumer**
   ```bash
   python part2_producer_consumer.py
   ```
3. **Part 3: Dining Philosophers**
   ```bash
   python part3_dining_philosophers.py
   ```
4. **Part 4: Thread Pool**
   ```bash
   python part4_thread_pool.py
   ```

You can view the execution output screenshots in the `screenshots/` directory.

---

## Part 1: Race Condition
This program demonstrates how a race condition occurs when multiple threads modify a shared counter without synchronization. It runs two scenarios: one without locks (yielding incorrect results) and one with `threading.Lock` (yielding correct results).

**Observations:**
I learned that without a lock, the final counter value is unpredictable and often incorrect because threads read stale values before incrementing. Adding a lock ensures that only one thread can access the critical section at a time, guaranteeing data integrity.

## Part 2: Producer-Consumer
This program simulates a bakery using a `queue.Queue`. Bakers (producers) add bread to the queue, and Customers (consumers) remove it. The queue has a fixed size (maxsize=5).

**Observations:**
The `queue.Queue` module is very helpful because it handles synchronization internally. When the basket is full, bakers automatically wait (block), and when it's empty, customers wait. This prevents overflow and underflow errors without needing complex manual lock management.

## Part 3: Dining Philosophers
This program solves the Dining Philosophers problem where 3 philosophers share 3 forks. Deadlock is prevented by using a resource hierarchy strategy.

**Observations:**
I learned that deadlock happens if every philosopher picks up their left fork simultaneously and waits indefinitely for the right one. By forcing a strict order (always picking up the lower-numbered fork first), we break the circular dependency condition, ensuring that at least one philosopher can always eat.

## Part 4: Thread Pool
This program compares sequential execution of tasks against parallel execution using `concurrent.futures.ThreadPoolExecutor`.

**Observations:**
Parallel execution provided a significant speedup (approx 3-4x with 4 workers) for these tasks. I simulated work using `time.sleep` (I/O bound), which is where Python threads shine. Sequential execution took about 10 seconds (1s * 10 tasks), while parallel execution took roughly 3 seconds, demonstrating the power of concurrency.