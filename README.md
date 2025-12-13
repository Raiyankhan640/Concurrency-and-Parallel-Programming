# Concurrency Assignment - [Raiyan]

## How to Run
- **Part 1:** `python part1_race_condition.py`
- **Part 2:** `python part2_producer_consumer.py`
- **Part 3:** `python part3_dining_philosophers.py`
- **Part 4:** `python part4_thread_pool.py`

## Part 1: Race Condition and Basic Synchronization
This program demonstrates a classic race condition where multiple threads try to update a shared counter at the same time.

### What I Learned
When I ran the code without the lock, the final value wasn't 3000 as expected. This happened because of the "race condition" - threads were reading the old value of the counter before another thread finished updating it, causing some increments to be lost.

To fix this, I used a `threading.Lock`. By putting the `increment` logic inside a `with self.lock:` block, I made sure that only one thread could touch the counter at a time. This gave me the correct result of 3000 every single time.

## Part 2: Producer-Consumer Problem
This simulation models a bakery where bakers produce bread and customers buy it, sharing a limited-size basket.

### What I Learned
I used a `queue.Queue` for the basket, which made things much easier because it is already thread-safe. I observed that:
- If the basket is full (5 items), the baker thread automatically waits (blocks) until there is space.
- If the basket is empty, the customer thread waits until new bread is baked.

This built-in synchronization prevented any "overflow" (putting too much bread) or "underflow" (taking from an empty basket) errors without me needing to write complex locking code.

## Part 3: Dining Philosophers
This is a solution to the famous Dining Philosophers problem, preventing deadlocks.

### What I Learned
I used the **Resource Hierarchy** solution to prevent deadlocks. The rule I implemented is simple: every philosopher must pick up their lower-numbered fork first.

For example, if Philosopher 2 sits between fork 2 and fork 0, they must pick up fork 0 first. This prevents the "circular wait" situation where everyone is holding one fork and waiting for the next, which is what causes deadlocks. This simple rule ensures the simulation runs forever without getting stuck.

## Part 4: Thread Pool for Parallel Tasks
This program compares running tasks one-by-one (sequential) vs. running them all at once (parallel) using a thread pool.

### What I Learned
I saw a huge difference in performance!
- **Sequential Execution:** Took longer because it had to wait for each task (like sleeping 1 second) to finish before starting the next.
- **Parallel Execution:** Was much faster (approx 3-4x speedup) because I used a thread pool with 4 workers. While one task was sleeping, other threads could pick up new tasks.

This showed me that for tasks that wait a lot (like I/O or sleep), using threads is much more efficient than doing things linearly.