"""
Dining Philosophers Problem Solution
This module implements a deadlock-free solution to the Dining Philosophers problem
using the Resource Hierarchy (or "numbered forks") approach.
"""

import threading
import time
import random

class DiningPhilosophers:
    """
    A simulation of the Dining Philosophers problem with deadlock prevention.
    Uses the Resource Hierarchy solution where forks are numbered and
    philosophers always pick up the lower-numbered fork first.
    """
    
    def __init__(self, num_philosophers=3, meals_per_philosopher=3):
        """
        Initialize the dining philosophers simulation.
        
        Args:
            num_philosophers (int): Number of philosophers (and forks).
            meals_per_philosopher (int): Number of times each philosopher eats.
        """
        self.num_philosophers = num_philosophers
        self.meals_per_philosopher = meals_per_philosopher
        self.forks = [threading.Lock() for _ in range(num_philosophers)]
        self.philosopher_threads = []
        self.simulation_complete = threading.Event()
        
    def philosopher(self, philosopher_id):
        """
        Philosopher thread function representing a dining philosopher.
        
        Args:
            philosopher_id (int): Unique identifier for the philosopher (0-based).
        """
        # Identify the philosopher's left and right forks
        left_fork_id = philosopher_id
        right_fork_id = (philosopher_id + 1) % self.num_philosophers
        
        # Determine fork order based on Resource Hierarchy solution
        # Always pick up lower-numbered fork first
        first_fork_id = min(left_fork_id, right_fork_id)
        second_fork_id = max(left_fork_id, right_fork_id)
        
        # Get the actual lock objects
        first_fork = self.forks[first_fork_id]
        second_fork = self.forks[second_fork_id]
        
        for meal_number in range(self.meals_per_philosopher):
            # Thinking phase
            think_time = random.uniform(1.0, 2.5)
            print(f"Philosopher {philosopher_id} is thinking (meal {meal_number + 1}/{self.meals_per_philosopher})...")
            time.sleep(think_time)
            
            # Hungry phase
            print(f"Philosopher {philosopher_id} is hungry and attempting to pick up forks...")
            
            # Pick up forks in order (Resource Hierarchy solution)
            first_fork.acquire()
            print(f"Philosopher {philosopher_id} picked up fork {first_fork_id}")
            
            second_fork.acquire()
            print(f"Philosopher {philosopher_id} picked up fork {second_fork_id}")
            
            # Eating phase
            eat_time = random.uniform(1.0, 2.0)
            print(f"Philosopher {philosopher_id} is EATING for {eat_time:.1f} seconds...")
            time.sleep(eat_time)
            
            # Put down forks (reverse order is not required but good practice)
            second_fork.release()
            print(f"Philosopher {philosopher_id} put down fork {second_fork_id}")
            
            first_fork.release()
            print(f"Philosopher {philosopher_id} put down fork {first_fork_id}")
            
            print(f"Philosopher {philosopher_id} finished meal {meal_number + 1}\n")
        
        print(f"Philosopher {philosopher_id} has finished all meals and is leaving the table.")
    
    def run(self):
        """
        Run the complete dining philosophers simulation.
        """
        print("=" * 60)
        print("DINING PHILOSOPHERS SIMULATION - Deadlock Prevention")
        print("=" * 60)
        print("Solution: Resource Hierarchy (Numbered Forks)")
        print(f"Configuration: {self.num_philosophers} philosophers, {self.meals_per_philosopher} meals each")
        print("-" * 60)
        
        # Create and start philosopher threads
        self.philosopher_threads = []
        for i in range(self.num_philosophers):
            philosopher_thread = threading.Thread(
                target=self.philosopher,
                args=(i,),
                name=f"Philosopher-{i}"
            )
            self.philosopher_threads.append(philosopher_thread)
            philosopher_thread.start()
            time.sleep(0.1)  # Stagger thread starts slightly
        
        # Wait for all philosophers to finish
        for philosopher_thread in self.philosopher_threads:
            philosopher_thread.join()
        
        print("=" * 60)
        print("SIMULATION COMPLETE - All philosophers have finished dining!")
        print(f"Total philosophers: {self.num_philosophers}")
        print(f"Total meals consumed: {self.num_philosophers * self.meals_per_philosopher}")
        print("=" * 60)
        print("\nDEADLOCK PREVENTION EXPLANATION:")
        print("-" * 60)
        print("The Resource Hierarchy solution prevents deadlock by:")
        print("1. Numbering all forks (resources) from 0 to N-1")
        print("2. Each philosopher always picks up the lower-numbered fork first")
        print("3. This creates a global ordering of resource acquisition")
        print("4. Circular wait condition cannot occur, preventing deadlock")
        print("-" * 60)

if __name__ == "__main__":
    """
    Main execution block for the Dining Philosophers simulation.
    Demonstrates deadlock prevention using the Resource Hierarchy solution.
    """
    # Create and run simulation
    dining_table = DiningPhilosophers(num_philosophers=3, meals_per_philosopher=3)
    dining_table.run()